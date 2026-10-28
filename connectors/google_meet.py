"""Read generated Meet transcripts and Gemini notes through Meet and Drive GETs.

Only conferences organized by the authorized user are discoverable. Artifacts
must already have been generated; this connector never enables transcription.
The credential is an OAuth access token, not an API key. It must be renewed
externally when it expires; no refresh token or write scope is used here.
Each poll replays the recent window to catch delayed artifacts and edited Docs.
Meet conference records expire after 30 days, even though Docs can live longer.
The calendar meeting at the same time shows them (meeting_notes.py): Gemini's notes under Notes, the transcript
under Transcript, marked From Google Meet, next to anything the owner added there and never in its place.
"""
import copy
import datetime as dt
import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request

KINDS = {'google_meet.transcript': 'Meet transcript', 'google_meet.notes': 'Meet notes'}
SETUP = {
    'label': 'Google Meet',
    'what': 'Meeting transcripts and Gemini notes from Google Meet.',
    'account': {'id': 'google-meet', 'service': 'google_meet', 'transport': 'api',
                'boundary': 'work', 'credential': 'google_meet', 'poll_seconds': 900},
    'ask': [],
    'secret': 'Google OAuth access token',
    'note': 'Turn on the Google Meet API and the Google Drive API at https://console.cloud.google.com/apis/library . '
            'Get an access token at https://developers.google.com/oauthplayground/ with the scopes '
            'https://www.googleapis.com/auth/meetings.space.readonly and '
            'https://www.googleapis.com/auth/drive.meet.readonly . An API key can\'t read private meetings. '
            'The token expires after about an hour: paste a new one then. '
            'It reads transcripts and notes of meetings you organized in the last 7 days. Meet keeps them for 30 days.',
    'hints': {'google_meet_http:HTTP_401': 'Google rejected the access token: paste a new one',
              'google_meet_http:HTTP_403': 'Google refused: turn on both APIs and allow both read-only scopes'}}
PAGE_SIZE = 10
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


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Never forward the access token to a location supplied by a response.
        return None


class Source:
    def __init__(self, config, account, helpers):
        self.helpers = helpers
        try:
            token = helpers.credential(config, account.get('credential', 'google_meet')).strip()
            if not re.fullmatch(r'[A-Za-z0-9._~+/-]+=*', token):
                raise ValueError
        except Exception:
            raise helpers.SourceError('google_meet_credential_unavailable') from None
        self.headers = {'Authorization': 'Bearer ' + token, 'User-Agent': 'TheMachine/1'}
        self.opener = urllib.request.build_opener(NoRedirect())

    def get(self, path, params=None, document=False):
        if document:
            allowed = re.fullmatch(r'files/' + ID + r'/export', path)
            base = 'https://www.googleapis.com/drive/v3/'
            params = {'mimeType': 'text/plain'}
        else:
            allowed = re.fullmatch(CONFERENCE + r'/(?:transcripts|smartNotes)', path) or path == 'conferenceRecords'
            base = 'https://meet.googleapis.com/v2/'
        if not allowed:
            raise self.helpers.SourceError('google_meet_path_not_allowed')
        url = base + path + ('?' + urllib.parse.urlencode(params) if params else '')
        request = urllib.request.Request(url, headers={**self.headers,
                                         'Accept': 'text/plain' if document else 'application/json'}, method='GET')
        try:
            with self.opener.open(request, timeout=30) as response:
                raw = response.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raise self.helpers.SourceError('google_meet_response_too_large')
            return raw.decode('utf-8-sig') if document else json.loads(raw)
        except urllib.error.HTTPError as error:
            retry = error.headers.get('Retry-After', '') if error.headers else ''
            # A generic 400/404/410 is not evidence of cursor expiry.
            expired = False
            if error.code == 400 and (params or {}).get('pageToken'):
                try:
                    message = json.loads(error.read(100_000))['error']['message'].lower()
                    expired = bool(re.search(r'page[ _-]?token', message) and
                                   re.search(r'\b(?:invalid|expired)\b', message))
                except (ValueError, KeyError, TypeError, AttributeError, OSError):
                    pass
            error.close()
            if expired:
                raise self.helpers.SourceError('google_meet_cursor_expired') from None
            delay = min(3600, max(1, int(retry))) if retry.isdigit() else (60 if error.code == 429 else None)
            raise self.helpers.SourceError('google_meet_http', error.code, retry_after=delay) from None
        except (urllib.error.URLError, TimeoutError, OSError):
            raise self.helpers.SourceError('google_meet_network') from None
        except (ValueError, UnicodeError):
            raise self.helpers.SourceError('google_meet_invalid_response') from None

    def page(self, path, key, params=None):
        page = self.get(path, params)
        if not isinstance(page, dict):
            raise self.helpers.SourceError('google_meet_invalid_page')
        items, token = page.get(key, []), page.get('nextPageToken', '')
        if (not isinstance(items, list) or not all(isinstance(item, dict) for item in items)
                or not isinstance(token, str) or (token and token == (params or {}).get('pageToken'))):
            raise self.helpers.SourceError('google_meet_invalid_page')
        return items, token


def artifact_event(source, account, conference, item, collection):
    helpers = source.helpers
    name = item.get('name')
    if not isinstance(name, str) or not re.fullmatch(re.escape(conference['name']) + '/' + collection + '/' + ID, name):
        raise helpers.SourceError('google_meet_invalid_artifact')
    if item.get('state') != 'FILE_GENERATED':
        return None
    destination = item.get('docsDestination')
    document = destination.get('document') if isinstance(destination, dict) else None
    if not isinstance(document, str) or not re.fullmatch(ID, document):
        raise helpers.SourceError('google_meet_invalid_document')
    occurred = timestamp(item.get('startTime') or conference['startTime'], helpers).isoformat()
    body = source.get('files/' + document + '/export', document=True).strip()
    # Do not collect explicitly labeled passwords or one-time codes in Docs.
    body = re.sub(r'(?i)\b(password|passcode|one[- ]time code|verification code|otp)\s*[:=]\s*\S+',
                  r'\1: [omitted]', body)
    notes = collection == 'smartNotes'
    cap = NOTES_CHARS if notes else TRANSCRIPT_CHARS
    # The conference's own times, so the calendar meeting is matched by when the call ran
    span = {'start_at': conference['startTime'], **({'end_at': conference['endTime']} if conference.get('endTime') else {})}
    return {'account_id': account['id'], 'source_id': hashlib.sha256(name.encode()).hexdigest(),
            'kind': 'google_meet.notes' if notes else 'google_meet.transcript',
            'occurred_at': occurred, 'title': ('Meeting notes' if notes else 'Meeting transcript') + ' · ' + occurred[:10],
            'body': body[:cap], 'deleted': False,
            'metadata': {'source_url': 'https://docs.google.com/document/d/' + document + '/edit',
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
        records, token = source.page('conferenceRecords', 'conferenceRecords', params)
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
    items, token = source.page(conference['name'] + '/' + collection, collection, params)
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
    """Read-only setup check; it does not create events or advance a checkpoint."""
    source = Source(config, account, helpers)
    records, _ = source.page('conferenceRecords', 'conferenceRecords', {'pageSize': 1})
    if records:
        record = records[0]
        name = record.get('name')
        if not isinstance(name, str) or not re.fullmatch(CONFERENCE, name):
            raise helpers.SourceError('google_meet_invalid_conference')
        for collection in ('transcripts', 'smartNotes'):
            items, _ = source.page(name + '/' + collection, collection, {'pageSize': 1})
            for item in items:
                artifact_event(source, account, record, item, collection)
