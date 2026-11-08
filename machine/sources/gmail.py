"""Gmail as a source: its API client (Gmail), a message as an event (message_event, list_headers) and its sync
(sync_gmail). Moved out of assistant.py as is."""
import base64
import datetime as dt
import html
import time
import urllib.parse

import bounces
from machine.sources.exclusions import email_subject_excluded
from machine.sources.rows import SKIPPED, Skips
from machine.text import QUOTED_HISTORY_KEPT, email_body, trim_quoted_history
from sources import SourceError, gog_read
from timeutil import now


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
    and Precedence; and Auto-Submitted, that a program sent it. Lowercased header names, as message_event reads them."""
    found = {}
    if headers.get('list-unsubscribe', '').strip():
        found['list_unsubscribe'] = True
    if headers.get('list-id', '').strip():
        found['list_id'] = ' '.join(headers['list-id'].split())[:200]
    if headers.get('precedence', '').strip():
        found['precedence'] = headers['precedence'].strip().lower()[:20]
    if headers.get('auto-submitted', '').strip().lower() not in ('', 'no'):
        found['auto_submitted'] = True  # an auto-reply or other mail a program sent (RFC 3834)
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
    if headers.get('reply-to'):
        metadata['reply-to'] = headers['reply-to']
    metadata.update(list_headers(headers))
    report = bounces.read_report(raw.get('payload'))  # a delivery report (bounce): its recipients, read from its structure
    if report:
        metadata['bounce'] = report
    metadata.update(thread_id=raw.get('threadId'), labels=sorted(raw.get('labelIds', [])),
                    source_url=raw.get('webLink') if account.get('service') == 'outlook' else
                    'https://mail.google.com/mail/u/?authuser=' + urllib.parse.quote(account['email']) + '#all/' + raw['id'],
                    truncated=len(body) > 40000, quoted_history_chars=quoted,
                    quoted_history_shortened=quoted > QUOTED_HISTORY_KEPT)
    return {'account_id': account['id'], 'source_id': raw['id'], 'kind': 'gmail.message',
            'occurred_at': dt.datetime.fromtimestamp(int(raw['internalDate']) / 1000, dt.timezone.utc).isoformat(),
            'title': headers.get('subject', '(no subject)')[:1000],
            'body': (body or raw.get('snippet', ''))[:40000], 'metadata': metadata,
            'deleted': False}


def sync_gmail(store, config, account):
    source = Gmail(config, account)
    profile = source.profile()  # Fail closed on account routing before every batch.
    state = store.checkpoint(account['id']) or {}
    excluded, skipped = set(), Skips('invalid_message')  # a message it can't take is counted, never holding up the page
    if not state:
        state = {'mode': 'bootstrap', 'base_history': str(profile['historyId']),
                 'after': int(time.time()) - config.get('bootstrap_days', 7) * 86400}
        store.commit_page(account['id'], state, [], record_sync=False)
    if state['mode'] in ['bootstrap', 'resync']:
        params = {'q': 'after:' + str(state['after']), 'maxResults': 40}
        if state.get('page_token'):
            params['pageToken'] = state['page_token']
        try:
            page = source.get('messages', params)
        except SourceError as error:
            if error.status == 400 and state.get('page_token'):
                state.pop('page_token')
                store.commit_page(account['id'], state, [], record_sync=False)
            raise
        events = []
        for ref in page.get('messages', []):
            event = skipped.take(message_event, account, source.get('messages/' + ref['id'], {'format': 'full'}), config)
            if event is SKIPPED: continue
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
            page = source.get('history', params)
        except SourceError as error:
            if error.status == 404:
                # Gmail can expire history cursors. Replay the retained time window (rolling,
                # not since first install); do not infer deletions from a partial mailbox scan.
                after = max(int(state['after']), int(time.time()) - config.get('bootstrap_days', 7) * 86400)
                store.commit_page(account['id'], {'mode': 'resync', 'base_history': str(profile['historyId']),
                                                  'after': after, 'resync_reason': 'expired_history'}, [], record_sync=False)
                return {'mode': 'resync', 'events': 0}
            raise
        changes = {}
        for record in page.get('history', []):
            for kind in ['messagesAdded', 'labelsAdded', 'labelsRemoved', 'messagesDeleted']:
                for item in record.get(kind, []):
                    changes[item['message']['id']] = kind
        events = []
        for source_id, kind in changes.items():
            try:
                event = store.tombstone(account['id'], source_id) if kind == 'messagesDeleted' else skipped.take(
                    message_event, account, source.get('messages/' + source_id, {'format': 'full'}), config)
            except SourceError as error:
                if error.status != 404:
                    raise
                event = store.tombstone(account['id'], source_id)
            if event is SKIPPED: continue
            if event:
                events.append(event)
            elif kind != 'messagesDeleted':
                excluded.add(source_id)
        next_state = {**state, 'page_token': page['nextPageToken']} if page.get('nextPageToken') else {
            **state, 'history_id': str(page.get('historyId', profile['historyId']))}
        if not page.get('nextPageToken'):
            next_state.pop('page_token', None)
    skipped.check().note(next_state)
    store.commit_page(account['id'], next_state, events, excluded_source_ids=excluded)
    return {'mode': next_state['mode'], 'events': len(events), 'filtered': len(excluded), 'skipped': sum(skipped.values())}
