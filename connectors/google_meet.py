"""Google Meet transcripts and Gemini notes, read with Meet's own Google sign-in.

Meet signs in on its own, apart from Gmail and Calendar: The Machine's Google Meet app asks for two read-only scopes,
and nothing else asks for them. Its refresh token is kept here (mail_grants.py, provider google_meet) and access tokens
come from its own broker (google_meet_broker, google_api.py), as for Zoom. Gmail's and gog's scopes stay as they are.

- https://www.googleapis.com/auth/meetings.space.readonly: conference records, their participants, transcripts and
  transcript entries, and smart notes (the Meet REST API).
- https://www.googleapis.com/auth/documents.readonly: the Gemini notes Google Doc, by the document id its smart notes
  record names (the Docs API). No Drive scope: never drive.readonly or the restricted drive.meet.readonly.

Only conferences the owner can see are discoverable. Artifacts must already have been generated; this connector never
enables transcription and never writes. Each poll replays the recent window to catch delayed artifacts and edited Docs.
Meet conference records expire after 30 days, even though Docs can live longer.
The calendar meeting at the same time shows them (meeting_notes.py): Gemini's notes under Notes, the transcript
under Transcript, marked From Google Meet, next to anything the owner added there and never in its place.

Config (a hosted Machine gets it from its control plane; a paired self-hosted one from pairing):
    "google_meet_broker": {"url": "https://app.example.com/api/google-meet/token"},
    "credentials": {"google_meet-broker": "~/.local/share/personal-assistant/google-broker"}
"""
import copy
import datetime as dt
import hashlib
import json
import re

KINDS = {'google_meet.transcript': 'Meet transcript', 'google_meet.notes': 'Meet notes'}
MEET_SCOPE = 'https://www.googleapis.com/auth/meetings.space.readonly'
DOCS_SCOPE = 'https://www.googleapis.com/auth/documents.readonly'
SCOPES = (MEET_SCOPE, DOCS_SCOPE)
PROVIDER = 'google_meet'  # its own sign-in and broker (google_api.py), never Gmail's
SETUP = {
    'label': 'Google Meet',
    'what': 'Meeting transcripts and Gemini notes from Google Meet.',
    'account': {'id': 'google-meet', 'service': 'google_meet', 'transport': 'broker', 'boundary': 'work', 'poll_seconds': 900},
    'note': 'Sign in with Google and allow reading Meet and Google Docs.',
    'ask': [('email', 'The Google address you meet with')],
    # Connect Google Meet: on a hosted Machine under + Add (its control plane's own sign-in); on a paired self-hosted one
    # the same through the control plane (fleet.SIGNIN_OF, onboarding.connect_grant)
    'account_page': 'source-google_meet',
    'hints': {'google_meet_not_connected': 'Connect Google Meet again',
              'google_meet_signin_expired': 'Connect Google Meet again'}}
PAGE_SIZE = 10
ENTRY_PAGE = 100     # transcript entries per request (Google's most)
ENTRY_PAGES = 60     # at most 6,000 entries of one transcript
PEOPLE_PAGES = 5     # participants per conference: 5 pages of 100
PAGES = 20
MAX_BYTES = 10_000_000
NOTES_CHARS = 40_000
TRANSCRIPT_CHARS = 400_000  # a long meeting's full transcript fits, as from Zoom
ID = r'[A-Za-z0-9_-]+'
CONFERENCE = r'conferenceRecords/' + ID


def timestamp(value, helpers):
    try:
        parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
        if parsed.tzinfo is None:
            raise ValueError
        return parsed.astimezone(dt.timezone.utc)
    except (ValueError, TypeError, AttributeError):
        raise helpers.SourceError('google_meet_invalid_timestamp') from None


def signin(config, account, helpers):
    """The sign-in to call with: Meet's own, for the account's address (mail_grants provider google_meet)."""
    email = str(account.get('email') or '').strip().lower()
    if not email or account.get('transport') != 'broker':
        raise helpers.SourceError('google_meet_not_connected')  # a token pasted before: connect Google Meet again
    return {'id': account['id'], 'email': email, 'transport': 'broker'}


class Source:
    def __init__(self, config, account, helpers):
        import google_api
        self.api, self.config, self.helpers = google_api, config, helpers
        self.signin = signin(config, account, helpers)
        self.people = {}  # participant resource name -> display name, for this run only

    def get(self, method, params, scope=MEET_SCOPE):
        """One GET through google_api (fixed methods, Google's hosts only, never a redirect elsewhere): parsed JSON."""
        helpers = self.helpers
        try:
            raw = self.api.call(self.config, helpers.credential, self.signin, method, params, scope, timeout=30,
                                raw=True, limit=MAX_BYTES, provider=PROVIDER)
        except self.api.BrokerError as error:
            category, status = error.category, error.status
            if category == 'google_scope_not_granted':
                raise helpers.SourceError('google_meet_not_connected', status) from None
            if category in ('google_broker_not_configured', 'google_broker_not_https', 'google_signin_unreadable') or \
                    (category == 'google_broker' and status == 404):
                raise helpers.SourceError('google_meet_not_connected') from None
            if status == 401:
                raise helpers.SourceError('google_meet_signin_expired', 401) from None
            if category == 'response_too_large':
                raise helpers.SourceError('google_meet_response_too_large') from None
            if category in ('unsupported_google_method', 'unsupported_google_url', 'missing_google_parameter'):
                raise helpers.SourceError('google_meet_path_not_allowed') from None
            if status == 400 and (params or {}).get('pageToken'):
                raise helpers.SourceError('google_meet_cursor_expired') from None
            if status:
                wait = getattr(error, 'retry_after', None)  # Google's Retry-After, when it gave one
                raise helpers.SourceError('google_meet_http', status, retry_after=wait or (60 if status == 429 else None)) from None
            raise helpers.SourceError('google_meet_network') from None
        try:
            return json.loads(raw.decode('utf-8-sig'))
        except (ValueError, UnicodeError):
            raise helpers.SourceError('google_meet_invalid_response') from None

    def page(self, method, params, key, scope=MEET_SCOPE):
        page = self.get(method, params, scope)
        if not isinstance(page, dict):
            raise self.helpers.SourceError('google_meet_invalid_page')
        items, token = page.get(key, []), page.get('nextPageToken', '')
        if (not isinstance(items, list) or not all(isinstance(item, dict) for item in items)
                or not isinstance(token, str) or (token and token == (params or {}).get('pageToken'))):
            raise self.helpers.SourceError('google_meet_invalid_page')
        return items, token

    def names(self, conference):
        """Who spoke: each participant's display name, as Meet shows it."""
        if conference in self.people:
            return self.people[conference]
        found, token = {}, ''
        for _ in range(PEOPLE_PAGES):
            items, token = self.page('meet.conferenceRecords.participants.list',
                                     {'conference': conference.split('/', 1)[1], 'pageSize': 100, **({'pageToken': token} if token else {})},
                                     'participants')
            for item in items:
                person = item.get('signedinUser') or item.get('anonymousUser') or item.get('phoneUser') or {}
                name = person.get('displayName') if isinstance(person, dict) else None
                if isinstance(item.get('name'), str) and isinstance(name, str) and name.strip():
                    found[item['name']] = ' '.join(name.split())[:80]
            if not token:
                break
        self.people[conference] = found
        return found

    def transcript(self, conference, name):
        """The transcript's text from its entries (Meet REST API), one line per turn: "Name: what they said"."""
        people, lines, token, size = self.names(conference), [], '', 0
        for _ in range(ENTRY_PAGES):
            items, token = self.page('meet.conferenceRecords.transcripts.entries.list',
                                     {'conference': conference.split('/', 1)[1], 'transcript': name.rsplit('/', 1)[1],
                                      'pageSize': ENTRY_PAGE, **({'pageToken': token} if token else {})}, 'transcriptEntries')
            for item in items:
                text = ' '.join(str(item.get('text') or '').split())
                if not text:
                    continue
                speaker = people.get(item.get('participant'), 'Someone')
                if lines and lines[-1][0] == speaker:
                    lines[-1][1].append(text)
                else:
                    lines.append((speaker, [text]))
                size += len(text) + 1
            if not token or size > TRANSCRIPT_CHARS:
                break
        return '\n'.join(f'{speaker}: {" ".join(said)}' for speaker, said in lines)

    def document(self, document):
        """The Gemini notes doc's text (Docs API, documents.readonly): its first tab, paragraphs and tables in order."""
        doc = self.get('docs.documents.get', {'documentId': document}, DOCS_SCOPE)
        if not isinstance(doc, dict):
            raise self.helpers.SourceError('google_meet_invalid_response')
        return doc_text((doc.get('body') or {}).get('content') if isinstance(doc.get('body'), dict) else None)


def doc_text(content, depth=0):
    """Plain text of a Docs API body: text runs, people and links as their names, table cells on their own lines."""
    out = []
    for element in content if isinstance(content, list) and depth < 8 else []:
        if not isinstance(element, dict):
            continue
        paragraph = element.get('paragraph')
        if isinstance(paragraph, dict):
            for part in paragraph.get('elements') or []:
                if not isinstance(part, dict):
                    continue
                run = part.get('textRun') or {}
                person = (part.get('person') or {}).get('personProperties') or {}
                link = (part.get('richLink') or {}).get('richLinkProperties') or {}
                text = run.get('content') if isinstance(run, dict) else None
                text = text if isinstance(text, str) else person.get('name') or person.get('email') or link.get('title') or ''
                out.append(text if isinstance(text, str) else '')
        table = element.get('table')
        if isinstance(table, dict):
            for row in table.get('tableRows') or []:
                for cell in (row.get('tableCells') or []) if isinstance(row, dict) else []:
                    if isinstance(cell, dict):
                        out.append(doc_text(cell.get('content'), depth + 1).strip() + '\n')
        toc = element.get('tableOfContents')
        if isinstance(toc, dict):
            out.append(doc_text(toc.get('content'), depth + 1))
    return ''.join(out)


def artifact_event(source, account, conference, item, collection):
    helpers = source.helpers
    name = item.get('name')
    if not isinstance(name, str) or not re.fullmatch(re.escape(conference['name']) + '/' + collection + '/' + ID, name):
        raise helpers.SourceError('google_meet_invalid_artifact')
    if item.get('state') != 'FILE_GENERATED':
        return None
    notes = collection == 'smartNotes'
    destination = item.get('docsDestination')
    document = destination.get('document') if isinstance(destination, dict) else None
    if notes and not isinstance(document, str) or document is not None and not (isinstance(document, str) and re.fullmatch(ID, document)):
        raise helpers.SourceError('google_meet_invalid_document')  # a transcript's doc is only linked: its entries are read
    occurred = timestamp(item.get('startTime') or conference['startTime'], helpers).isoformat()
    body = (source.document(document) if notes else source.transcript(conference['name'], name)).strip()
    # Do not collect explicitly labeled passwords or one-time codes in Docs.
    body = re.sub(r'(?i)\b(password|passcode|one[- ]time code|verification code|otp)\s*[:=]\s*\S+',
                  r'\1: [omitted]', body)
    cap = NOTES_CHARS if notes else TRANSCRIPT_CHARS
    # The conference's own times, so the calendar meeting is matched by when the call ran
    span = {'start_at': conference['startTime'], **({'end_at': conference['endTime']} if conference.get('endTime') else {})}
    return {'account_id': account['id'], 'source_id': hashlib.sha256(name.encode()).hexdigest(),
            'kind': 'google_meet.notes' if notes else 'google_meet.transcript',
            'occurred_at': occurred, 'title': ('Meeting notes' if notes else 'Meeting transcript') + ' · ' + occurred[:10],
            'body': body[:cap], 'deleted': False,
            'metadata': {**({'source_url': 'https://docs.google.com/document/d/' + document + '/edit'} if document else {}),
                         'thread_id': hashlib.sha256(conference['name'].encode()).hexdigest(),
                         'conference': conference['name'], 'artifact': name,
                         'truncated': len(body) > cap, 'body_chars': len(body), **span}}


def window(now, days, since=None):
    after = now - dt.timedelta(days=days)
    if since is not None:
        # An outage must not silently discard meetings outside the overlap.
        after = min(after, since - dt.timedelta(seconds=1))
    after = max(after, now - dt.timedelta(days=30))
    return {'after': after.isoformat(), 'before': now.isoformat(),
            'pending': [], 'conference_token': '', 'conferences_done': False,
            'collection': 'transcripts', 'artifact_token': ''}


def collect_page(source, account, current):
    """Advance one list page. The checkpoint keeps only opaque IDs and times."""
    if not current['pending']:
        params = {'pageSize': PAGE_SIZE,
                  'filter': f'start_time>="{current["after"]}" AND start_time<="{current["before"]}"'}
        if current['conference_token']:
            params['pageToken'] = current['conference_token']
        records, token = source.page('meet.conferenceRecords.list', params, 'conferenceRecords')
        pending = []
        after = timestamp(current['after'], source.helpers)
        before = timestamp(current['before'], source.helpers)
        for record in records:
            name = record.get('name')
            if not isinstance(name, str) or not re.fullmatch(CONFERENCE, name):
                raise source.helpers.SourceError('google_meet_invalid_conference')
            start = timestamp(record.get('startTime'), source.helpers).isoformat()
            # endTime is there once the call has ended
            end = timestamp(record['endTime'], source.helpers).isoformat() if record.get('endTime') else None
            if after <= timestamp(start, source.helpers) <= before:
                pending.append({'name': name, 'startTime': start, **({'endTime': end} if end else {})})
        current.update(pending=pending, conference_token=token, conferences_done=not token)
        return []
    conference, collection = current['pending'][0], current['collection']
    params = {'pageSize': PAGE_SIZE}
    if current['artifact_token']:
        params['pageToken'] = current['artifact_token']
    items, token = source.page('meet.conferenceRecords.' + collection + '.list',
                               {'conference': conference['name'].split('/', 1)[1], **params}, collection)
    events = [event for item in items if (event := artifact_event(source, account, conference, item, collection))]
    current['artifact_token'] = token
    if not token:
        if collection == 'transcripts':
            current['collection'] = 'smartNotes'
        else:
            current['pending'].pop(0)
            current['collection'] = 'transcripts'
    return events


def sync(store, config, account, helpers):
    source = Source(config, account, helpers)
    state = copy.deepcopy(store.checkpoint(account['id']) or {})
    now = timestamp(helpers.now(), helpers)
    try:
        days = int(config.get('bootstrap_days', 7))
        if days < 1:
            raise ValueError
    except (ValueError, TypeError, OverflowError):
        raise helpers.SourceError('google_meet_invalid_window') from None
    if days > 30:
        state['coverage_gap'] = 'Meet retains conference records for 30 days; older meetings cannot be discovered.'
    days = min(days, 30)
    if 'window' not in state:
        since = timestamp(state['since'], helpers) if state.get('since') else None
        if since is not None and since < now - dt.timedelta(days=30):
            state['coverage_gap'] = 'Collection was offline beyond Meet\'s 30-day retention; older meetings may be missing.'
        state['window'] = window(now, days, since)
    count, resets = 0, 0
    for _ in range(PAGES):
        current = state['window']
        try:
            events = collect_page(source, account, current)
        except helpers.SourceError as error:
            if error.category != 'google_meet_cursor_expired' or resets:
                raise
            resets += 1
            state.update(cursor_expired_at=now.isoformat(), window=window(now, days))
            state['coverage_gap'] = 'An expired page token required a recent-window replay; older pending artifacts may be missing.'
            state['coverage_complete'] = False
            store.commit_page(account['id'], state, [])
            continue
        count += len(events)
        done = not current['pending'] and current['conferences_done']
        state.update(mode='incremental', coverage_complete=done and not state.get('coverage_gap'),
                     coverage='Recent Meet artifact window collected.' if done else 'Meet artifact pages are still being collected.')
        if done:
            state['since'] = current['before']
            del state['window']
        store.commit_page(account['id'], state, events)
        if done:
            break
    return {'mode': 'incremental', 'events': count, 'more': 'window' in state}


def check(config, account, helpers):
    """Read-only setup check; it does not create events or advance a checkpoint. Both scopes must be granted: the
    notes doc is read with the second one, which a first meeting without notes would not show."""
    source = Source(config, account, helpers)
    try:
        granted = source.api.scopes(config, helpers.credential, source.signin, provider=PROVIDER)
    except source.api.BrokerError as error:
        not_here = error.status == 404 or error.category in ('google_broker_not_configured', 'google_broker_not_https')
        raise helpers.SourceError('google_meet_not_connected' if not_here else 'google_meet_network', error.status) from None
    if not set(SCOPES) <= granted:
        raise helpers.SourceError('google_meet_not_connected', 403)
    records, _ = source.page('meet.conferenceRecords.list', {'pageSize': 1}, 'conferenceRecords')
    if records:
        record = records[0]
        name = record.get('name')
        if not isinstance(name, str) or not re.fullmatch(CONFERENCE, name):
            raise helpers.SourceError('google_meet_invalid_conference')
        for collection in ('transcripts', 'smartNotes'):
            items, _ = source.page('meet.conferenceRecords.' + collection + '.list',
                                   {'conference': name.split('/', 1)[1], 'pageSize': 1}, collection)
            for item in items:
                artifact_event(source, account, record, item, collection)
