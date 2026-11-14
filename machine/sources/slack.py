"""Slack as a source: the Web API client (Slack), its messages as events (slack_event), the order, pacing and first
import steps of its channels, and the names of Slack members in text (slack_named, slack_ids_named, slack_named_out).
The sync itself (sync_slack) and the title writes to the sealed events table stay in assistant.py, which imports these
names back. Moved out of assistant.py as is."""
import datetime as dt
import hashlib
import html
import http.client
import json
import os
from pathlib import Path
import random
import re
import socket
import sqlite3
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

import graph
from machine import stamps
from sources import SourceError, credential, rate_limited, transient
from timeutil import now


# Slack's read limit, per transport: The Machine's own Slack app (Sign in with Slack, `broker`) and Maton's. Slack allows
# an app outside its Marketplace about one conversations.history or .replies read a minute per workspace, 15 messages a
# page. read_seconds: at most one such read this often by default (config slack_read_seconds overrides it, never under
# floor); page: messages asked for per read. When The Machine's Slack app is approved for the Marketplace, the `broker`
# row is the only thing to change (Slack's Tier 3: 50+ reads a minute, up to 200 messages a page); Maton keeps its own.
SLACK_LIMITS = {'broker': {'read_seconds': 180, 'floor': 65, 'page': 15},
                'maton': {'read_seconds': 180, 'floor': 65, 'page': 15}}


def slack_limits(account):
    return SLACK_LIMITS['broker' if (account or {}).get('transport') == 'broker' else 'maton']


def slack_rounds_path(config):
    return Path(config['database']).expanduser().parent / 'slack-rounds.json' if config.get('database') else None


def slack_rounds_kept(config):
    """{account id: its round and minute} as Slack.keep_round saved them."""
    path = slack_rounds_path(config)
    try:
        found = json.loads(path.read_text()) if path else {}
    except (OSError, ValueError):
        return {}
    return found if isinstance(found, dict) else {}


# A run waiting on its asked reads (slack_read 'reading') sleeps at most this long before it asks again, and READ_WAIT_MARGIN
# on top of the reads it waits for: a read already under way, and the collector's turn after its pause.
READ_WAIT_MAX, READ_WAIT_MARGIN = 300, 30


def slack_read_wait(config, account, waiting):
    """Seconds a to-do's run waits before it asks again for its Slack conversations (slack_read 'reading'). The
    connection reads one conversation every slack_read_seconds (3 minutes by default), or every round it learned after
    Slack's 429s (Slack.read_went), the asked ones first: `waiting` asked conversations take about that many reads. A
    run that waited 195 seconds for two of them found both still reading and stopped with "paste the update here"
    (2026-11-14): two take two reads."""
    limits = slack_limits(account)
    every = max(limits['floor'], int(config.get('slack_read_seconds', limits['read_seconds'])))
    kept = slack_rounds_kept(config).get(str((account or {}).get('id')))
    if isinstance(kept, dict) and kept.get('base') == every:
        try:
            every = max(every, min(int(kept.get('round') or every), Slack.SLACK_ROUND_MAX))
        except (TypeError, ValueError):
            pass
    return min(READ_WAIT_MAX, max(1, waiting) * every + READ_WAIT_MARGIN)


class Slack:
    METHODS = {'auth.test', 'users.info', 'users.conversations', 'conversations.history',
               'conversations.replies', 'conversations.info'}
    # Seconds between two calls of a method, by Slack's tier for it: users.conversations is Tier 2 (20 a minute), the
    # others here allow more. A first import lists a large workspace's conversations page after page: at the 2 seconds
    # every other call waits, that went over Tier 2 and came back as 429s.
    CALL_GAP = {'users.conversations': 3.5}

    def __init__(self, config, account, stop=None):
        self.config, self.account, self.stop = config, account, stop
        self.verified_until = 0
        self.last_call = 0
        limits = slack_limits(account)
        # Conservative non-Marketplace limits match this connection's observed
        # one-success-per-minute replies. Warm up after restart rather than
        # forgetting a request sent just before shutdown.
        # Slack allows such an app about one history or replies read a minute per workspace, shared
        # by every computer on the same connection (an own install and a hosted server, later a
        # whole Fleet) and by anything else reading through it, like a scheduled post that checks
        # the channel first. So this collector spends at most one of those reads every
        # slack_read_seconds (default 3 minutes) and leaves the rest of the minute to others.
        self.limited_reads = {'conversations.history', 'conversations.replies'}
        # The collector and the history backfill (machine/app/history.py history_slack) share this client, so one
        # limited read waits for the other's: never two in Slack's minute.
        self.limited_lock = threading.Lock()
        self.read_seconds = max(limits['floor'], int(config.get('slack_read_seconds', limits['read_seconds'])))
        self.last_limited = time.monotonic()
        # Machines on one workspace (a team's hosted servers, an own install) share that one read a minute. Each reads
        # in its own minute of a round, on the clock: a slot picked from this Machine and connection. A 429 means
        # another Machine reads in that minute or the round is too short for all of them: the round doubles (up to
        # SLACK_ROUND_MAX) and this one takes another slot. Rounds are the base round times a power of two, so a
        # longer round's minutes are a subset of a shorter one's slot and Machines on different rounds can still
        # each have their own minutes (with a minute or so added, a 3- and a 4-minute round met every 12 minutes).
        # It halves again only after SLACK_CALM reads and SLACK_CALM_SECONDS without one. What it learned is kept
        # in slack-rounds.json next to the database: a release restarts a team's Machines together, and starting
        # over from the first slot each time brought the same 429s back right after every update (2026-10-28).
        self.round, self.calm, self.limited_at = self.read_seconds, 0, 0.0
        self.slots = max(1, self.round // 60)
        self.slot = int(hashlib.sha256(f"{socket.gethostname()}|{account.get('connection_id') or account.get('id')}".encode()).hexdigest(), 16) % self.slots
        kept = self.rounds_kept().get(str(account.get('id')))
        if isinstance(kept, dict) and kept.get('base') == self.read_seconds:
            try:
                rounds = int(kept['round']) // self.read_seconds
                if self.read_seconds <= int(kept['round']) <= self.round_max() and rounds & (rounds - 1) == 0 and 0 <= int(kept['slot']) < int(kept['round']) // 60:
                    self.round, self.slot, self.limited_at = int(kept['round']), int(kept['slot']), float(kept.get('limited_at') or 0)
                    self.slots = max(1, self.round // 60)
            except (KeyError, TypeError, ValueError):
                pass

    SLOT_OPEN = 20  # seconds into its minute a read may still start
    SLACK_ROUND_MAX = 720  # a read every twelve minutes, room for a dozen Machines on one workspace
    SLACK_CALM = 30
    SLACK_CALM_SECONDS = 12 * 3600

    def round_max(self):
        rounds = 1
        while self.read_seconds * rounds * 2 <= max(self.SLACK_ROUND_MAX, self.read_seconds):
            rounds *= 2
        return self.read_seconds * rounds

    def rounds_path(self):
        return slack_rounds_path(self.config)

    def rounds_kept(self):
        return slack_rounds_kept(self.config)

    def keep_round(self):
        """Save this connection's round and minute, so a restart reads in the same minute."""
        path = self.rounds_path()
        if not path:
            return
        try:
            found = self.rounds_kept()
            found[str(self.account.get('id'))] = {'base': self.read_seconds, 'round': self.round, 'slot': self.slot, 'limited_at': self.limited_at}
            temp = path.with_name(path.name + '.tmp')
            fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, 'w') as handle:
                handle.write(json.dumps(found))
            os.replace(temp, path)
        except OSError:
            pass  # pacing still works for this run

    def slot_wait(self, at):
        """Seconds from `at` (epoch) until this Machine's minute of the round, 0 within its first SLOT_OPEN seconds."""
        if self.slots < 2:
            return 0
        into = (at - self.slot * 60) % self.round
        return 0 if into < self.SLOT_OPEN else self.round - into

    def read_went(self, limited):
        """After a history or replies read: Slack refused it for the rate limit (limited) or took it."""
        if limited:
            self.round, self.calm, self.limited_at = min(self.round_max(), self.round * 2), 0, time.time()
            before, self.slots = self.slot, max(1, self.round // 60)
            if self.slots > 1:
                self.slot = random.choice([n for n in range(self.slots) if n != before])
            self.keep_round()
        elif self.round > self.read_seconds:
            self.calm += 1
            if self.calm >= self.SLACK_CALM and time.time() - self.limited_at >= self.SLACK_CALM_SECONDS:
                self.round, self.calm = self.round // 2, 0
                self.slots = max(1, self.round // 60)
                self.slot %= self.slots
                self.keep_round()

    def limited_gap(self):
        """Seconds after a limited read before the next one may go (its own minute of the round comes on top)."""
        return self.round if self.slots < 2 else 65

    def limited_wait(self, stamp=None):
        """Seconds a history or replies read would wait now (pace) for this connection's turn."""
        stamp = time.monotonic() if stamp is None else stamp
        delay = max(0, 2 - (stamp - self.last_call), self.limited_gap() - (stamp - self.last_limited))
        # with minutes in a round: never two reads within Slack's minute, then this Machine's own minute (after a restart too)
        return delay + self.slot_wait(time.time() + delay) if self.slots > 1 else delay

    def pace(self, method):
        stamp = time.monotonic()
        delay = self.limited_wait(stamp) if method in self.limited_reads else max(0, self.CALL_GAP.get(method, 2) - (stamp - self.last_call))
        if self.stop is not None:
            if self.stop.wait(delay):
                raise SourceError('collector_stopped')
        else:
            time.sleep(delay)
        self.last_call = time.monotonic()
        if method in self.limited_reads:
            self.last_limited = self.last_call

    def request(self, method, values, fresh=False):
        """The GET for one Web API method: straight to Slack with the owner's own sign-in (Sign in with Slack,
        slack_api.py), or through Maton for an account connected there before."""
        if self.account.get('transport') == 'broker':
            import slack_api
            try:
                token = slack_api.broker_token(self.config, self.account, fresh=fresh)[0]
            except slack_api.TokenError as error:
                raise SourceError(error.label, error.status, error.retry_after) from None
            return urllib.request.Request(slack_api.API + method + ('?' + values if values else ''),
                                          headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/json'})
        secret = credential(self.config, self.account['credential'])
        variable = self.account['credential_variable']
        matches = re.findall(r'^' + re.escape(variable) + r'=(.*)$', secret, re.M)
        if len(matches) != 1:
            raise SourceError('slack_credential_unavailable')
        secret = matches[0].strip().strip('"\'')
        return urllib.request.Request('https://api.maton.ai/slack/api/' + method +
            ('?' + values if values else ''), headers={
                'Authorization': 'Bearer ' + secret,
                'Maton-Connection': self.account['connection_id'], 'Accept': 'application/json'})

    def get(self, method, params=None):
        if method not in self.METHODS:
            raise SourceError('slack_method_not_allowed')
        if method in self.limited_reads:
            with self.limited_lock:
                return self.read(method, params)
        return self.read(method, params)

    def read(self, method, params):
        self.pace(method)
        values = urllib.parse.urlencode(params or {})
        broker = self.account.get('transport') == 'broker'
        request = self.request(method, values)
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                if not broker and response.headers.get('Maton-Connection') != self.account['connection_id']:
                    raise SourceError('connection_identity_mismatch')
                data = json.load(response)
            if broker and isinstance(data, dict) and data.get('error') in ('invalid_auth', 'token_expired', 'token_revoked'):
                # the access token ran out early or the sign-in was renewed elsewhere: one fresh one, then Slack's answer
                with urllib.request.urlopen(self.request(method, values, fresh=True), timeout=45) as response:
                    data = json.load(response)
        except urllib.error.HTTPError as error:
            try:
                retry_after = max(60, min(3600, int(error.headers.get('Retry-After', '300'))))
            except ValueError:
                retry_after = 300
            if error.code == 429:
                # Spread out computers that share the connection, so they don't all retry at once.
                retry_after += random.randint(5, 60)
                if method in self.limited_reads:
                    self.read_went(True)
            raise SourceError('slack:' + method, error.code, retry_after) from None
        except (urllib.error.URLError, TimeoutError, http.client.HTTPException) as error:
            # Keep only the exception class and an allowlisted read method,
            # never exception messages, endpoints, credentials or response bodies.
            cause = error.reason if isinstance(error, urllib.error.URLError) else error
            name = type(cause).__name__ if isinstance(cause, BaseException) else 'Unknown'
            if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,60}', name):
                name = 'Unknown'
            raise SourceError('network:' + name + ':' + method) from None
        except ValueError:
            raise SourceError('invalid_json') from None
        if not isinstance(data, dict) or not data.get('ok'):
            label = data.get('error') if isinstance(data, dict) else None
            known = {'ratelimited', 'invalid_cursor', 'thread_not_found', 'channel_not_found', 'user_not_found', 'user_not_visible',
                     'not_in_channel', 'missing_scope', 'invalid_auth', 'token_revoked', 'token_expired'} | SLACK_ACCOUNT_LABELS | SLACK_HICCUP_LABELS
            if label == 'ratelimited' and method in self.limited_reads:
                self.read_went(True)
            raise SourceError('slack_' + (label if label in known else 'invalid_response') + ':' + method,
                              retry_after=60 if label == 'ratelimited' else None)
        if method in self.limited_reads:
            self.read_went(False)
        return data

    EMAIL_GRACE = 6 * 3600  # seconds a passed email check carries a users.info hiccup (Slack's or the network's)

    def profile(self):
        if time.monotonic() < self.verified_until:
            return
        identity = self.get('auth.test')
        if (identity.get('team_id') != self.account['team_id'] or
                identity.get('user_id') != self.account['user_id'] or identity.get('bot_id')):
            raise SourceError('account_identity_mismatch')
        try:
            user = self.get('users.info', {'user': self.account['user_id']}).get('user', {})
        except SourceError as error:
            # auth.test just confirmed the workspace and member. When Slack or the network then hiccups on users.info
            # (internal_error, a timeout) and this member's email passed the check shortly before, the reads go on and
            # the next sync checks again. It used to fail every sync for as long as Slack kept answering
            # internal_error there (2026-11-11). A first check, or any other answer, still fails closed.
            verified = getattr(self, 'email_verified_at', 0)
            if verified and time.monotonic() - verified < self.EMAIL_GRACE and slack_hiccup(error):
                return
            raise
        if user.get('profile', {}).get('email', '').lower() != self.account['email'].lower():
            raise SourceError('account_identity_mismatch')
        self.email_verified_at = time.monotonic()
        self.verified_until = self.email_verified_at + 300


def slack_raw_title(event):
    """The title a Slack message had before members were named in it: what its content hash is taken over, so naming
    someone (slack_event, name_slack_titles) never makes a message look new or edited."""
    body = str(event.get('body') or '')
    return ('#' + str(event['metadata'].get('channel_name') or '') + ': ' + (body.splitlines()[0] if body else '(message)'))[:1000]


def slack_event(account, channel, raw, names=None):
    """names: {Slack member id: name} (graph.slack_names): the title names people, never their member id."""
    stamp = raw.get('message', raw) if raw.get('subtype') == 'message_changed' else raw
    ts = stamp.get('ts')
    if not ts or not re.fullmatch(r'\d+\.\d+', ts):
        raise SourceError('invalid_slack_timestamp')
    body = html.unescape(stamp.get('text', ''))
    metadata = {'channel_id': channel['id'], 'channel_name': channel['name'],
                'conversation_type': channel['type'], 'user_id': stamp.get('user'),
                'bot_id': stamp.get('bot_id'), 'subtype': stamp.get('subtype'),
                'message_ts': ts, 'thread_ts': stamp.get('thread_ts', ts),
                'edited_at': stamp.get('edited', {}).get('ts'),
                'reply_count': stamp.get('reply_count', 0), 'latest_reply': stamp.get('latest_reply'),
                'source_url': 'https://' + account['slack_host'] + '/archives/' + channel['id'] +
                              '/p' + ts.replace('.', '').ljust(16, '0'),
                'truncated': len(body) > 40000}
    if channel.get('external'):
        metadata['slack_connect'] = True  # shared with another company (Slack Connect): may be a client conversation
    title = graph.slack_title(channel['name'], body, names or {})
    return {'account_id': account['id'], 'source_id': channel['id'] + ':' + ts,
            'kind': 'slack.message', 'occurred_at': dt.datetime.fromtimestamp(float(ts), dt.timezone.utc).isoformat(),
            'title': title, 'body': body[:40000], 'metadata': metadata, 'deleted': False}


def slack_error(error):
    """The Slack error label without the method it came from ('slack_not_in_channel:conversations.history')."""
    return error.category.split(':', 1)[0]


# Slack's error labels, by what they are about (https://docs.slack.dev/reference/methods/conversations.history).
# The sign-in or the whole workspace: every conversation would answer the same, so the sync fails and the connection says so.
SLACK_ACCOUNT_LABELS = {'account_inactive', 'not_authed', 'no_permission', 'org_login_required', 'ekm_access_denied',
                        'team_access_not_granted', 'two_factor_setup_required', 'enterprise_is_restricted', 'accesslimited'}
# Slack's own trouble, answered as a label instead of a 5xx: the same read is tried again, like a 5xx or a timeout.
SLACK_HICCUP_LABELS = {'internal_error', 'fatal_error', 'service_unavailable', 'request_timeout'}
# One conversation: the owner left it or was removed (channel_not_found, not_in_channel), the sign-in has no scope for
# its kind (missing_scope: Slack's history scopes are per kind of conversation), a label not named above
# (invalid_response: the account was checked just before, see Slack.profile), or a page that says there is more without
# saying where (missing_cursor). The others are read all the same.
SLACK_REFUSED = ('slack_channel_not_found', 'slack_not_in_channel', 'slack_missing_scope', 'slack_invalid_response',
                 'slack_missing_cursor')
SLACK_REFUSED_REST = 3600  # after a first refusal; doubles each time, up to a day
SLACK_GONE_AFTER = 3  # refusals in a row before a conversation the owner's list no longer has is dropped


def slack_refused(error):
    """Slack's answer is about this one conversation (SLACK_REFUSED), not about the connection."""
    return slack_error(error) in SLACK_REFUSED


def slack_hiccup(error):
    """Slack or the network, as far as anyone can tell (a 5xx, a timeout, Slack's internal_error): the same call is
    worth another try later. Never a rate limit: that waits for its Retry-After and the read's round."""
    label = slack_error(error)
    return not rate_limited(error) and (transient(error) or label == 'invalid_json'
                                        or label[len('slack_'):] in SLACK_HICCUP_LABELS)


SLACK_HICCUP_REST = 120  # seconds a direct message whose check hiccuped waits before it is checked again


def slack_set_aside(config, channel, label):
    """A conversation Slack refused: it says so (the Slack card counts it as unavailable) and rests, longer each time
    in a row, so it never comes first again while the others wait. Its next read that works clears it."""
    channel['refused'] = int(channel.get('refused') or 0) + 1
    rest = min(86400, SLACK_REFUSED_REST * 2 ** min(channel['refused'] - 1, 10))
    channel.update(error=label, due=time.time() + max(rest, slack_interval(config, channel)))


def slack_prune(state, listed):
    """After Slack listed every conversation the owner is in (a complete users.conversations, `listed`): one that is
    no longer among them and was refused SLACK_GONE_AFTER times in a row leaves the list. What was read from it stays.
    Never on one refusal, and never from a list that is empty or incomplete."""
    listed = set(listed or ())
    if listed:
        state['channels'] = [c for c in state['channels'] if c['id'] in listed or not c.get('error')
                             or int(c.get('refused') or 0) < SLACK_GONE_AFTER]


def slack_turn_done(state):
    """A conversation's turn ended, read or set aside: on to the next one, and after the last one the regular rounds."""
    state.pop('scan', None)
    state['index'] += 1
    if state.get('step'):
        slack_first_import_next(state)
    elif state['index'] >= len(state['channels']):
        state.update(index=0, mode='incremental')
        if time.time() >= state.get('next_discovery', 0):
            state['phase'] = 'discover'


def slack_activity(channel):
    """Best guess of when someone last wrote in a conversation: messages read so far, else the first import's hint."""
    return max(float(channel.get('last_activity') or 0), float(channel.get('hint') or 0))


def slack_order(channels):
    """Your own notes first, then by how recently anyone wrote: today, this week, older. Within each, direct
    messages before group chats before channels, newest first."""
    now, kinds = time.time(), {'dm': 0, 'group': 1}
    def key(c):
        seen = slack_activity(c)
        age = 0 if seen >= now - 86400 else 1 if seen >= now - 7 * 86400 else 2
        return (c['name'] != 'My notes', age, kinds.get(c['type'], 2), -seen, c['name'])
    channels.sort(key=key)


SLACK_FIRST_STEPS = ('recent', 'deepen', 'quiet')


def slack_first_import_plan(config, state):
    """The first import's plan, so signals start within minutes rather than hours. Slack allows about one read a
    minute, so the reads go where the activity is: conversations active today get their last day first
    ('recent'), then the rest of the window ('deepen'), together with those active this week. Quiet ones come
    last ('quiet'). A direct message with nothing in the window is skipped: its newest message is known."""
    now = time.time()
    window = now - config.get('bootstrap_days', 7) * 86400
    for c in state['channels']:
        seen = slack_activity(c)
        if c['type'] == 'dm' and seen < window and not c.get('last_scan'):
            c['first'] = 'skip'
            c.update(last_scan=f'{now:.6f}', next_full=now + 86400)
            if seen:
                c['last_activity'] = seen
            c['due'] = now + slack_interval(config, c)
        else:
            c['first'] = 'recent' if seen >= now - 86400 else 'full' if seen >= window else 'quiet'
    slack_order(state['channels'])
    state.pop('triage', None)
    state.update(phase='scan', index=0, step='recent')
    slack_first_import_next(state)


def slack_first_import_wanted(channel, step):
    first = channel.get('first')
    if step == 'recent':
        return first == 'recent' and not channel.get('last_scan')
    if step == 'deepen':
        return bool(channel.get('deepen')) or (first == 'full' and not channel.get('last_scan'))
    return first == 'quiet' and not channel.get('last_scan')


def slack_first_import_next(state):
    """Moves state['index'] to the next conversation the first import still wants, through its steps in turn.
    After the last one, the first import is done and the regular rounds take over."""
    while True:
        while state['index'] < len(state['channels']):
            if slack_first_import_wanted(state['channels'][state['index']], state['step']):
                return
            state['index'] += 1
        position = SLACK_FIRST_STEPS.index(state['step'])
        if position + 1 == len(SLACK_FIRST_STEPS):
            state.pop('step')
            state.update(index=0, mode='incremental')
            if time.time() >= state.get('next_discovery', 0):
                state['phase'] = 'discover'
            return
        state.update(step=SLACK_FIRST_STEPS[position + 1], index=0)


def slack_first_import_progress(state):
    """Where the first import is, for the Slack card: the step, how many of its conversations are done, and how
    many quiet ones wait for the end."""
    channels = state.get('channels') or []
    if state.get('phase') == 'triage':
        return {'step': 'triage', 'done': state.get('triage', 0), 'total': len(channels), 'quiet': 0}
    step = state.get('step')
    if not step:
        return None
    first = [c.get('first') for c in channels]
    quiet = sum(f == 'quiet' and not c.get('last_scan') for f, c in zip(first, channels))
    if step == 'recent':
        mine = [c for f, c in zip(first, channels) if f == 'recent']
        done = sum(bool(c.get('last_scan')) for c in mine)
    elif step == 'deepen':
        mine = [c for f, c in zip(first, channels) if f in ('recent', 'full')]
        done = sum(bool(c.get('last_scan')) and not c.get('deepen') for c in mine)
    else:
        mine = [c for f, c in zip(first, channels) if f == 'quiet']
        done = len(mine) - quiet
    return {'step': step, 'done': done, 'total': len(mine), 'quiet': quiet}


def slack_interval(config, channel):
    """How long a conversation rests after a read, by how recently anyone wrote in it: busy ones
    are read again within the hour, quiet ones once a day. Direct messages are checked more often,
    with a cheap call that doesn't count toward Slack's one-read-a-minute limit."""
    if channel.get('type') == 'dm':
        return config.get('slack_dm_check_minutes', 10) * 60
    age = time.time() - float(channel.get('last_activity') or 0)
    if age < 86400:
        return config.get('slack_active_minutes', 60) * 60
    if age < 7 * 86400:
        return config.get('slack_recent_hours', 6) * 3600
    return config.get('slack_quiet_hours', 24) * 3600


def slack_rest(config, channel):
    """How long a conversation may rest by how recently anyone wrote in it, a direct message too: the yardstick
    for how late a read is. (A direct message's 10-minute check is the cheap conversations.info call.)"""
    return max(60, slack_interval(config, {**channel, 'type': 'channel'}))


# Conversations a to-do's run asked to have read now (SyncApp.slack_read_action): {(account id, channel id): when it
# asked}. A quiet channel rests up to a day between reads, so a message posted there after its last read was nowhere to
# be found, and a run went looking in the browser instead (2026-11-09). In memory only: after a restart the run asks
# again. An ask counts until the conversation's next read starts after it, or for READ_NOW_MAX at most.
READ_NOW, READ_NOW_LOCK, READ_NOW_MAX = {}, threading.Lock(), 1800


def slack_read_now(account_id, channel_id):
    """Ask for this conversation's next read to come first; returns when it was asked (an earlier ask stands)."""
    with READ_NOW_LOCK:
        key = (account_id, channel_id)
        if key in READ_NOW and time.time() - READ_NOW[key] > READ_NOW_MAX:
            READ_NOW.pop(key)
        return READ_NOW.setdefault(key, time.time())


def slack_read_asked(account_id, channel):
    """When a run asked to have this conversation read, while that read is still to come; else None."""
    with READ_NOW_LOCK:
        at = READ_NOW.get((account_id, channel.get('id')))
        if at is not None and time.time() - at > READ_NOW_MAX:
            READ_NOW.pop((account_id, channel.get('id')))
            at = None
    return at if at is not None and float(channel.get('last_scan') or 0) < at else None


def slack_read_drop(account_id, channel_id):
    with READ_NOW_LOCK:
        READ_NOW.pop((account_id, channel_id), None)


def slack_next_due(store, config, account, source, state):
    """Moves state['index'] to the conversation that most needs a read and returns True, or returns False when
    nothing is due. Slack allows about one history read a minute (one every few minutes on a shared workspace),
    so the order matters: of the conversations that are due, the one latest for its own rest wins (an hour late
    for a busy channel weighs as much as a day for a quiet one), and a direct message with a new message goes
    first. A plain walk through the list in order let a daily batch of quiet conversations hold busy channels
    up for half a day (2026-11-05). Ties keep the list order from the current index. Skipping costs no Slack
    call, except for a direct message, where conversations.info shows its newest message: only a new one there
    makes it worth a history read, also for the daily full read when nothing in it is in the window anyway. A
    conversation a to-do's run asked for (slack_read_now) goes first, rested or not: the run waits on it."""
    now, channels = time.time(), state['channels']
    if now >= state.get('next_discovery', 0):
        state.update(phase='discover', index=0)
        store.commit_page(account['id'], state, [])
        return False
    retained = max(float(state.get('after') or 0), now - config.get('bootstrap_days', 7) * 86400)
    start, best, moved = state['index'] % len(channels), None, False
    hiccups, checked = [], False  # direct messages whose check hiccuped; whether any check answered
    for offset in range(len(channels)):
        i = (start + offset) % len(channels)
        channel = channels[i]
        if slack_read_asked(account['id'], channel) is not None:
            best = (float('inf'), i)
            break
        if now < channel.get('due', 0):
            continue
        news = False
        if channel.get('type') == 'dm' and channel.get('last_scan') and not channel.get('threads_waiting') \
                and isinstance(source, Slack):
            fresh = now < channel.get('next_full', 0)
            if fresh or not channel.get('threads'):
                try:
                    info = source.get('conversations.info', {'channel': channel['id']}).get('channel') or {}
                except SourceError as error:
                    # One check timing out (Slack or the network) failed the whole sync (2026-11-11): that direct
                    # message is checked again shortly and the others go on. Only when no check answered at all is it
                    # the connection, and the sync fails as before.
                    if slack_hiccup(error):
                        hiccups.append((channel, error))
                        continue
                    # A direct message this token can't open (closed, or with a removed member) failed every sync
                    # and held up every other conversation behind it (2026-11-09): it rests like a quiet one, and
                    # says it can't be read and rests longer each time (slack_set_aside), until a later read clears it
                    # or discovery drops it.
                    if not slack_refused(error):
                        raise
                    slack_set_aside(config, channel, slack_error(error))
                    moved = True
                    continue
                checked = True
                latest = info.get('latest') or {}
                newest = float(latest.get('ts') or 0)
                seen = max(float(channel.get('last_activity') or 0), float(channel['last_scan']))
                if newest <= seen and (fresh or newest < retained):
                    channel['due'] = now + slack_interval(config, channel)
                    if not fresh:
                        channel['next_full'] = now + 86400
                    moved = True
                    continue
                news = newest > seen
        rank = float('inf') if news else (now - channel.get('due', 0)) / slack_rest(config, channel)
        if best is None or rank > best[0]:
            best = (rank, i)
    if hiccups:
        if best is None and not checked:
            raise hiccups[0][1]
        for channel, _ in hiccups:
            channel['due'] = now + SLACK_HICCUP_REST
        moved = True
    if best is None:
        state['index'] = 0
        store.commit_page(account['id'], state, [])
        return False
    if moved or state['index'] != best[1]:
        state['index'] = best[1]
        store.commit_page(account['id'], state, [], record_sync=False)
    return True


def slack_page_names(store, channel, messages):
    """{Slack member id: name} for a page of messages: the DM's other person, the senders and whoever they mention."""
    ids = set(graph.slack_members_on({'channel_name': channel.get('name')}))
    for raw in messages:
        stamp = raw.get('message', raw) if raw.get('subtype') == 'message_changed' else raw
        ids.add(str(stamp.get('user') or ''))
        ids |= {m[0] for m in graph.SLACK_MENTION.findall(str(stamp.get('text') or ''))}
    try:
        with store.connect() as db:
            return graph.slack_names(db, ids)
    except sqlite3.Error:
        return {}


# A Slack member as the API names them: a message carries only this id, so a review or the dashboard reading it as is
# sees "U02AB3CD4", and once it wrote "Slack teammate U02AB3CD4" on a promise. Their names come from users.info, kept
# in identity_names (remember_slack_names): slack_named and slack_ids_named put the name in its place.
SLACK_ID = re.compile(r'\b(?:Slack (?:teammate|user|member|colleague|contact) )?([UW][A-Z0-9]{8,11})\b')


def slack_name_table(db, ids):
    """{user id: name} for these Slack member ids (graph.slack_names: the people graph, users.info, or the name kept for
    an app, the owner or a former member). Unknown ones are left out. Kept until a name, a person or a member changes:
    a page names the same few members on every open, and each time was a pass over every person."""
    key = tuple(sorted({i for i in ids if isinstance(i, str)}))
    return dict(_NAMES.get(key, stamps.stamp(db, ('identity_names', 'graph_nodes', 'slack_members')), lambda: graph.slack_names(db, key)))


_NAMES = stamps.Kept(64)


def slack_ids_named(db, text, names=None):
    """Text with each Slack member id it mentions ("Slack teammate U02AB3CD4", "DM U02AB3CD4", "<@U02AB3CD4>") as that
    person's name (graph.slack_text_named)."""
    text = str(text or '')
    found = graph.slack_ids_in(text)
    if not found:
        return text
    return graph.slack_text_named(text, names if names is not None else slack_name_table(db, found))


def _slack_link(match):
    target, label = match[1], (match[2] or '').strip()
    if target.startswith('#'):
        return '#' + (label or 'channel')
    if target.startswith('@'):
        return '@' + (label or graph.SOMEONE_ON_SLACK)
    if target.startswith('!'):
        return '@' + (label or target[1:].split('^')[0])
    if label:
        return label
    if target.startswith('mailto:'):
        return target[7:]
    parts = urllib.parse.urlsplit(target)
    return (parts.netloc.removeprefix('www.') + ('/…' if parts.path.strip('/') or parts.query else '')) if parts.netloc else target


def slack_plain(text):
    """Slack's mrkdwn as words people read in a list: "<https://x.example/a|the doc>" as "the doc", a bare link as
    "x.example/…", "<#C1|deals>" as "#deals", "<!here>" as "@here", *bold*, _italic_ and ~struck~ without their marks,
    and &amp; &lt; &gt; as the characters. Mentions are named first (slack_ids_named); one left is not shown as an id."""
    text = re.sub(r'<([^<>|\s]+)(?:\|([^<>]*))?>', _slack_link, str(text or ''))
    text = re.sub(r'(?<![\w*_~])([*_~])(?=\S)([^*_~\n]*?\S)\1(?![\w*_~])', r'\2', text)
    return html.unescape(text)


# Keys whose values are ids an agent passes back (event_id, channel_id, user_id, ...): kept as they are.
SLACK_KEPT_KEY = re.compile(r'(^|_)(id|ids|ts|user|channel|cursor|url|key)$')


def slack_named_out(db, value):
    """An action's result as an agent reads it: every Slack member id in its text by name ("<@U02AB3CD4>",
    "DM U02AB3CD4", "Slack teammate U02AB3CD4", a known bare id), whatever stored it (event bodies, earlier tool
    results, profile evidence, notes). Values under id keys stay, so the agent can still act on them."""
    try:
        ids = graph.slack_ids_in(json.dumps(value, ensure_ascii=False, default=str))
    except (TypeError, ValueError):
        return value
    if not ids:
        return value
    names = graph.slack_names(db, ids)

    def walk(v, key=''):
        if isinstance(v, str) and v[:1] in '{[' and v[-1:] in '}]':
            try:
                return json.dumps(walk(json.loads(v), key), ensure_ascii=False)  # metadata kept as JSON text: its id fields stay
            except ValueError:
                pass
        if isinstance(v, str):
            return v if SLACK_KEPT_KEY.search(key) else graph.slack_text_named(v, names)
        if isinstance(v, dict):
            return {k: walk(x, str(k)) for k, x in v.items()}
        if isinstance(v, (list, tuple)):
            return [walk(x, key) for x in v]
        return v
    return walk(value)


def slack_named(db, rows):
    """Slack messages with their sender's name (sender_display), a DM's other person and everyone they mention by name
    (title, body), as a WhatsApp message carries its sender: for the review, its earlier-in-conversation lines,
    preparations and the dashboard. Never a member id: one no name is known for is "someone on Slack". Other rows stay
    as they are."""
    slack = [r for r in rows if r.get('kind') == 'slack.message']
    if not slack:
        return rows
    meta = {id(r): (r['metadata'] if isinstance(r['metadata'], dict) else json.loads(r['metadata'] or '{}')) for r in slack}
    ids = {m.get('user_id') for m in meta.values()} | {i for r in slack for i in SLACK_ID.findall(str(r.get('title') or ''))} | {
        i for m in meta.values() for i in SLACK_ID.findall(str(m.get('channel_name') or ''))} | {
        i for r in slack for i in graph.slack_ids_in(r.get('body'))}
    names = slack_name_table(db, ids)
    out = []
    for r in rows:
        if r.get('kind') != 'slack.message':
            out.append(r)
            continue
        m = dict(meta[id(r)])
        if names.get(m.get('user_id')) and not m.get('sender_display'):
            m['sender_display'] = names[m['user_id']]
        if m.get('channel_name'):
            m['channel_name'] = graph.slack_text_named(m['channel_name'], names)
        title = r.get('title')
        if graph.slack_title_lost(title) and 'body' in r:  # stored before a name was known: made again from the message
            title = graph.slack_title(meta[id(r)].get('channel_name'), html.unescape(str(r['body'] or '')), names)
        named = {**r, 'title': graph.slack_text_named(title, names, graph.SOMEONE_ON_SLACK),
                 'metadata': m if isinstance(r['metadata'], dict) else json.dumps(m)}
        if 'body' in r:
            named['body'] = graph.slack_text_named(r['body'], names)  # mentions by name, for the review and preparations
        out.append(named)
    return out
