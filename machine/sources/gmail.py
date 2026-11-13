"""Gmail as a source: its API client (Gmail), a message as an event (message_event, list_headers) and its sync
(sync_gmail). Moved out of assistant.py as is."""
import base64
import datetime as dt
import html
import re
import time
import urllib.parse

import bounces
from machine.sources.exclusions import email_subject_excluded
from machine.sources.rows import SKIPPED, Skips
from machine.text import QUOTED_HISTORY_KEPT, _address, email_body, trim_quoted_history
import ms_graph
from sources import MICROSOFT_SERVICES, SourceError, gog_read, transient
from timeutil import now

AUTHUSER = re.compile(r'^https://mail\.google\.com/mail/u/\?authuser=([^#&]+)#')
THREAD = re.compile(r'[0-9a-f]{8,24}')


def phone_link(url, thread):
    """A Gmail message's link for a phone. On a phone mail.google.com serves its mobile site, which drops the desktop
    link's #all/<message> and lands in the inbox; the mobile site opens a conversation as #cv/<label>/<thread> (the
    thread's id, not the message's), in the account the link names. None when the link isn't Gmail's own."""
    account = AUTHUSER.match(str(url or ''))
    if not account or not THREAD.fullmatch(str(thread or '')):
        return None
    return f'https://mail.google.com/mail/mu/mp/?authuser={account[1]}#cv/All%20Mail/{thread}'


class Gmail:
    def __init__(self, config, account):
        self.config, self.account = config, account

    def get(self, resource, params=None):
        methods = {'profile': 'gmail.users.getProfile', 'messages': 'gmail.users.messages.list',
                   'history': 'gmail.users.history.list'}
        method = methods.get(resource, 'gmail.users.threads.get' if resource.startswith('threads/') else 'gmail.users.messages.get')
        values = {'userId': 'me', **(params or {})}
        if resource.startswith(('messages/', 'threads/')):
            values['id'] = resource.split('/')[1]
        return gog_read(self.config, self.account, 'gmail', 'v1', method, values,
                        'https://www.googleapis.com/auth/gmail.readonly')

    def profile(self):
        profile = self.get('profile')
        if profile.get('emailAddress', '').lower() != self.account['email'].lower():
            raise SourceError('account_identity_mismatch')
        if not profile.get('historyId'):
            raise SourceError('missing_history_id')
        return profile


def list_headers(headers):
    """What says a message went to a list: List-Unsubscribe (only that it is there, never its link or address), List-Id
    and Precedence; X-Original-From (or -Sender), who wrote a mail a list relayed; and Auto-Submitted, that a program
    sent it; X-The-Machine, that The Machine's own mailer sent it (machine_notice). Lowercased header names, as
    message_event reads them."""
    found = {}
    if headers.get('list-unsubscribe', '').strip():
        found['list_unsubscribe'] = True
    if headers.get('list-id', '').strip():
        found['list_id'] = ' '.join(headers['list-id'].split())[:200]
    if headers.get('precedence', '').strip():
        found['precedence'] = headers['precedence'].strip().lower()[:20]
    original = (headers.get('x-original-from') or headers.get('x-original-sender') or '').strip()
    if original:
        found['original_from'] = ' '.join(original.split())[:300]  # who wrote it, when a list relayed it (a Google Group)
    if headers.get('auto-submitted', '').strip().lower() not in ('', 'no'):
        found['auto_submitted'] = True  # an auto-reply or other mail a program sent (RFC 3834)
    if headers.get(NOTICE_HEADER, '').strip():
        found['machine_notice'] = True  # The Machine's own mailer sent it (machine_notice)
    return found


# The Machine's own purely informational mail to its owner: the morning digest and what still waits (notify.mail) and
# fix notices. The control plane's mailer sends it from NOTICE_DOMAIN and stamps NOTICE_HEADER on it, and only on it:
# billing, a trial ending, an invite or an account change come from the same address without it and may need a to-do.
NOTICE_HEADER = 'x-the-machine'
NOTICE_DOMAIN = 'themachine.computer'
MAIL_KINDS = frozenset({'gmail.message', 'ms_graph.message', 'outlook.message'})


def machine_notice(kind, metadata):
    """Informational mail The Machine itself sent the owner, known by its sender (an address at NOTICE_DOMAIN) together
    with its mailer's NOTICE_HEADER, never by its words. It tells the owner about what the dashboard already has: never
    read by the review (Store.commit_page marks it reviewed), so it costs no model turn and never shows in the last
    check's list. Both parts are needed: the header alone anyone can add, and the same address also sends mail that
    may need a to-do (billing, a trial ending, an invite), which has no header."""
    if kind not in MAIL_KINDS or not isinstance(metadata, dict):
        return False
    if set(metadata.get('labels') or ()) & {'SENT', 'DRAFT'} or metadata.get('from_me'):
        return False
    local, _, domain = _address(metadata.get('from')).rpartition('@')
    if not local or not (domain == NOTICE_DOMAIN or domain.endswith('.' + NOTICE_DOMAIN)):
        return False
    return bool(metadata.get('machine_notice'))


ATTACHMENTS_LISTED = 10  # names kept per message


def attachment_names(payload):
    """The files a message carries, by name and type only (never their bytes): the review can't open them, so this
    tells it a statement or invoice is in a file (AGENTS.md, "Bills to pay by hand") and a to-do's own run reads
    it. Pictures shown inline in the body (a logo, a signature) are left out."""
    found = []

    def walk(part):
        name = ' '.join(str(part.get('filename') or '').split())
        kind = str(part.get('mimeType') or '').lower()
        headers = {h.get('name', '').lower(): str(h.get('value', '')).lower() for h in part.get('headers', []) if isinstance(h, dict)}
        inline = headers.get('content-disposition', '').startswith('inline') or bool(headers.get('content-id'))
        if name and not (inline and kind.startswith('image/')) and len(found) < ATTACHMENTS_LISTED:
            found.append({'name': name[:120], 'type': kind[:80]})
        for child in part.get('parts', []) or []:
            walk(child)

    walk(payload or {})
    return found


def message_event(account, raw, config=None):
    headers = {h['name'].lower(): h.get('value', '')
               for h in raw.get('payload', {}).get('headers', [])}
    if email_subject_excluded(config or {}, headers.get('subject', '')):
        return None
    bodies = {'text/plain': [], 'text/html': []}

    def parts(part):
        # Attachment bytes, credentials and raw protocol dumps are not retained.
        if not part.get('filename') and part.get('mimeType') in bodies:
            data = part.get('body', {}).get('data', '')
            if data:
                try:
                    bodies[part['mimeType']].append(base64.urlsafe_b64decode(data + '=' * (-len(data) % 4))
                                                   .decode('utf-8', errors='replace'))
                except ValueError:
                    raise SourceError('invalid_message_encoding') from None
        for child in part.get('parts', []):
            parts(child)

    parts(raw.get('payload', {}))
    # Account-local literal exclusions, before selecting/truncating the body.
    # Check both MIME alternatives: a marker in HTML can be absent from plain text.
    terms = [term.casefold() for term in account.get('excluded_terms', []) if term]
    content = [raw.get('snippet', ''),
               *(h.get('value','') for h in raw.get('payload',{}).get('headers',[])),
               *bodies['text/plain'], *bodies['text/html']]
    if any(term in html.unescape(value).casefold() for term in terms for value in content):
        return None
    body, quoted = trim_quoted_history(email_body('\n'.join(bodies['text/plain']), bodies['text/html']), headers.get('subject', ''))
    metadata = {key: headers.get(key, '') for key in ['from', 'to', 'cc', 'date', 'message-id', 'in-reply-to']}
    for key in ('reply-to', 'bcc', 'sender'):  # the viewer's Details: Bcc on sent mail, a Sender that isn't the From
        if headers.get(key):
            metadata[key] = headers[key]
    metadata.update(list_headers(headers))
    report = bounces.read_report(raw.get('payload'))  # a delivery report (bounce): its recipients, read from its structure
    if report:
        metadata['bounce'] = report
    files = attachment_names(raw.get('payload'))
    if files:  # sealed at rest with the rest of what a message says (not in message_seal.PLAIN_METADATA)
        metadata['attachments'] = files
    metadata.update(thread_id=raw.get('threadId'), labels=sorted(raw.get('labelIds', [])),
                    source_url=raw.get('webLink') if account.get('service') in ('outlook', 'imap') else
                    'https://mail.google.com/mail/u/?authuser=' + urllib.parse.quote(account['email']) + '#all/' + raw['id'],
                    truncated=len(body) > 40000, quoted_history_chars=quoted,
                    quoted_history_shortened=quoted > QUOTED_HISTORY_KEPT)
    return {'account_id': account['id'], 'source_id': raw['id'], 'kind': 'gmail.message',
            'occurred_at': dt.datetime.fromtimestamp(int(raw['internalDate']) / 1000, dt.timezone.utc).isoformat(),
            'title': headers.get('subject', '(no subject)')[:1000],
            'body': (body or raw.get('snippet', ''))[:40000], 'metadata': metadata,
            'deleted': False}


ROUND_SECONDS = ms_graph.ROUND_SECONDS  # an Outlook mail round's time for Graph, its reads' retries included (ms_graph.budget)
FAILED_IN_A_ROW = 3  # messages whose reads failed one after another: Graph is down, the rest waits for the next round
WAITING_MAX = 100  # this many messages waiting: they are read before any new change is listed
READ_AT_MAX = 500
LATER = object()  # what Round.take gives for a message that waits for the next round


class Round:
    """One Outlook mail round against a Graph that fails part of its reads: for hours a mailbox can get a 5xx or no answer
    on about half of its requests, each served on another try. ms_graph retries every read a few times (budget); a message
    whose read still fails waits in the checkpoint ('waiting': since when, how often tried, its change's time) and is read
    again next round, while the cursor moves on and what was read is kept. After FAILED_IN_A_ROW failed messages, or once
    the round's time is up, the rest waits too. A waiting message is never dropped: it waits until it reads or is gone
    (404), and its 'since' shows one that keeps failing. A round that got nothing from Graph fails as before (transient,
    so only reported when that keeps happening); one that listed or read anything is a success, partial or not.
    'read_at' keeps the messages read at the cursor's own time, which the next listing (changed at or after it) gives
    again: they aren't read twice. Gmail fails the round on any failed read, as before."""

    def __init__(self, state, microsoft):
        self.microsoft = microsoft
        waiting = state.get('waiting') if microsoft else None
        self.waiting = {k: v for k, v in waiting.items() if isinstance(v, dict)} if isinstance(waiting, dict) else {}
        read_at = state.get('read_at') if microsoft else None
        self.read_at = read_at if isinstance(read_at, dict) and isinstance(read_at.get('ids'), list) else {}
        self.answered, self.failed, self.error, self.done = 0, 0, None, set()

    def full(self):
        return len(self.waiting) >= WAITING_MAX

    def stopped(self):
        left = ms_graph.left()
        return self.failed >= FAILED_IN_A_ROW or (left is not None and left <= 0)

    def seen(self, source_id, modified):
        return bool(modified) and modified == self.read_at.get('stamp') and source_id in self.read_at['ids']

    def take(self, source_id, read, modified=None):
        """read() for this message, or LATER when it waits for the next round (Outlook only)."""
        if not self.microsoft:
            return read()
        if self.stopped():
            self.wait(source_id, modified, tried=False)
            return LATER
        try:
            result = read()
        except SourceError as error:
            if not transient(error):
                raise
            self.failed, self.error = self.failed + 1, error
            self.wait(source_id, modified, tried=True)
            return LATER
        self.failed = 0
        self.answered += 1
        self.done.add(source_id)
        modified = modified or (self.waiting.pop(source_id, None) or {}).get('modified')
        self.waiting.pop(source_id, None)
        stamp = self.read_at.get('stamp')
        if modified and (not stamp or modified > stamp):
            self.read_at = {'stamp': modified, 'ids': [source_id]}
        elif modified and modified == stamp and source_id not in self.read_at['ids'] and len(self.read_at['ids']) < READ_AT_MAX:
            self.read_at['ids'].append(source_id)
        return result

    def gone(self, source_id):
        """Graph answered that this message is no more (404): it is tombstoned and waits no longer."""
        self.answered += 1
        self.done.add(source_id)
        self.waiting.pop(source_id, None)

    def wait(self, source_id, modified, tried):
        entry = self.waiting.get(source_id) or {'since': now(), 'tries': 0}
        self.waiting[source_id] = {**entry, 'tries': int(entry.get('tries') or 0) + int(tried), **({'modified': modified} if modified else {})}
        self.done.add(source_id)


def sync_gmail(store, config, account):
    microsoft = account.get('service') in MICROSOFT_SERVICES and bool(account.get('email'))
    if not microsoft:
        return _sync_mail(store, config, account, False)
    with ms_graph.budget(ROUND_SECONDS):
        return _sync_mail(store, config, account, True)


def _sync_mail(store, config, account, microsoft):
    source = Gmail(config, account)
    if microsoft:  # the address /me gave this connection before a restart, while it holds (ms_graph.IDENTITY_SECONDS)
        ms_graph.restore_identity(config, account, (store.checkpoint(account['id']) or {}).get('identity'))
    profile = source.profile()  # Fail closed on account routing before every batch.
    state = store.checkpoint(account['id']) or {}
    checked = ms_graph.checked_identity(config, account) if microsoft else None
    excluded, skipped = set(), Skips('invalid_message')  # a message it can't take is counted, never holding up the page
    if not state:
        state = {'mode': 'bootstrap', 'base_history': str(profile['historyId']),
                 'after': int(time.time()) - config.get('bootstrap_days', 7) * 86400}
        store.commit_page(account['id'], state, [], record_sync=False)
    turn, events, listed = Round(state, microsoft), [], False

    def read(source_id):
        return lambda: skipped.take(message_event, account, source.get('messages/' + source_id, {'format': 'full'}), config)

    def listing(resource, params):
        """The page of messages or changes, or None when this round reads only what waits (Outlook: Graph failed it)."""
        if turn.microsoft and turn.full():
            return None
        try:
            return source.get(resource, params)
        except SourceError as error:
            if not turn.microsoft or not transient(error):
                raise
            turn.error = error
            return None

    if state['mode'] in ['bootstrap', 'resync']:
        params = {'q': 'after:' + str(state['after']), 'maxResults': 40}
        if state.get('page_token'):
            params['pageToken'] = state['page_token']
        try:
            page = listing('messages', params)
        except SourceError as error:
            if error.status == 400 and state.get('page_token'):
                state.pop('page_token')
                store.commit_page(account['id'], state, [], record_sync=False)
            raise
        next_state = dict(state)
        if page is not None:
            listed = True
            for ref in page.get('messages', []):
                if ref['id'] in turn.done:
                    continue
                event = turn.take(ref['id'], read(ref['id']))
                if event is SKIPPED or event is LATER: continue
                if event is None:
                    excluded.add(ref['id'])
                else:
                    events.append(event)
            next_state = {**state, 'page_token': page['nextPageToken']} if page.get('nextPageToken') else {
                'mode': 'incremental', 'history_id': state['base_history'], 'after': state['after'],
                'resync_reason': state.get('resync_reason')}
            if state['mode'] == 'bootstrap' and not page.get('nextPageToken'):
                next_state['backfilled_at'] = now()  # the mailbox's first import is in: its first review starts now (App.mail_backfill)
    else:
        params = {'startHistoryId': state['history_id'], 'maxResults': 100}
        if state.get('page_token'):
            params['pageToken'] = state['page_token']
        try:
            page = listing('history', params)
        except SourceError as error:
            if error.status == 404:
                # Gmail can expire history cursors. Replay the retained time window (rolling,
                # not since first install); do not infer deletions from a partial mailbox scan.
                after = max(int(state['after']), int(time.time()) - config.get('bootstrap_days', 7) * 86400)
                store.commit_page(account['id'], {'mode': 'resync', 'base_history': str(profile['historyId']),
                                                  'after': after, 'resync_reason': 'expired_history',
                                                  **({'waiting': turn.waiting} if turn.waiting else {})}, [], record_sync=False)
                return {'mode': 'resync', 'events': 0}
            raise
        next_state = dict(state)
        if page is not None:
            listed = True
            changes, stamps = {}, {}
            for record in page.get('history', []):
                for kind in ['messagesAdded', 'labelsAdded', 'labelsRemoved', 'messagesDeleted']:
                    for item in record.get(kind, []):
                        changes[item['message']['id']] = kind
                        stamps[item['message']['id']] = item['message'].get('modified')  # Outlook's change time
            for source_id, kind in changes.items():
                if kind != 'messagesDeleted' and (source_id in turn.done or turn.seen(source_id, stamps[source_id])):
                    continue
                try:
                    event = store.tombstone(account['id'], source_id) if kind == 'messagesDeleted' else \
                        turn.take(source_id, read(source_id), stamps[source_id])
                except SourceError as error:
                    if error.status != 404:
                        raise
                    turn.gone(source_id)
                    event = store.tombstone(account['id'], source_id)
                if event is SKIPPED or event is LATER: continue
                if event:
                    events.append(event)
                elif kind != 'messagesDeleted':
                    excluded.add(source_id)
            next_state = {**state, 'page_token': page['nextPageToken']} if page.get('nextPageToken') else {
                **state, 'history_id': str(page.get('historyId', profile['historyId']))}
            if not page.get('nextPageToken'):
                next_state.pop('page_token', None)
    for source_id in sorted(turn.waiting, key=lambda k: int(turn.waiting[k].get('tries') or 0)):  # the least tried first
        if source_id in turn.done:
            continue
        try:
            event = turn.take(source_id, read(source_id))
        except SourceError as error:
            if error.status != 404:
                raise
            turn.gone(source_id)
            event = store.tombstone(account['id'], source_id)
        if event is SKIPPED or event is LATER: continue
        if event:
            events.append(event)
        else:
            excluded.add(source_id)
    skipped.check().note(next_state)
    next_state.pop('identity', None)
    if checked:
        next_state['identity'] = checked
    if microsoft:
        for key, value in (('waiting', turn.waiting), ('read_at', turn.read_at)):
            if value:
                next_state[key] = value
            else:
                next_state.pop(key, None)
        if turn.error and not (listed or turn.answered):  # nothing from Graph this round: a failure, keeping what waits
            store.commit_page(account['id'], next_state, events, record_sync=False, excluded_source_ids=excluded)
            raise turn.error
    store.commit_page(account['id'], next_state, events, excluded_source_ids=excluded)
    result = {'mode': next_state['mode'], 'events': len(events), 'filtered': len(excluded), 'skipped': sum(skipped.values())}
    if turn.waiting:
        result['waiting'] = len(turn.waiting)
        result['waiting_since'] = min(str(v.get('since') or '') for v in turn.waiting.values())
    if turn.error and turn.answered:
        result['more'] = True  # it stopped early or left some for later, and Graph answers again: the next round soon
    return result
