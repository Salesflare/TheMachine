"""Granola meeting notes: the notes Granola wrote for each meeting the owner was in, and its transcript when Granola
has one. Read only: GET requests to Granola's public API (https://docs.granola.ai/introduction), nothing is ever
written to Granola. The matching calendar meeting shows them in its Notes and Transcript, marked From Granola, next to
anything the owner added there, never over it (meeting_notes.py): by the calendar event Granola names, else by time.

The key is a personal API key the owner makes in Granola's desktop app (Settings, Connectors, API keys) with the
Personal notes scope; Granola gives these keys on its Business and Enterprise plans. Granola's API takes no OAuth
(its MCP server does, but answers in free text for a chat model, with no documented format). The key is treated as
opaque: any printable text without spaces, never a fixed prefix or length. Granola states no expiry for it: a key it
turns down (401) asks the owner for a new one.

    {"id": "granola", "service": "granola", "transport": "api", "boundary": "work", "credential": "granola",
     "poll_seconds": 900}

Granola's API has no "who am I": the key's own address (the card's name, and whose notes are theirs) is the owner of
the notes it lists (whose()), learned when it connects and on each run.

Each run lists the notes updated since the last one (a two-hour overlap; the first run reads bootstrap_days back) and
reads each new or changed one with its transcript. Only notes of meetings the owner was in come in: theirs, or one
that lists one of their addresses among its attendees or invitees. A note shared with them from a meeting they were
not in is skipped. Granola allows 5 requests a second: this reader paces itself under that.
"""
import datetime as dt
import hashlib
import http.client
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from machine import kinds as kind_rows

KINDS = {kind: row['name'] for kind, row in kind_rows.KINDS.items() if row['service'] == 'granola'}  # machine/kinds.py says
# How each kind reads in the message viewer (email, chat, notification or card) and the app its link opens in
# (machine/store/message_view.py; docs/adding-a-source.md, "How a message reads")
VIEWS = {kind: 'card' for kind in KINDS}
APP = 'Granola'
# Granola's own page on making an API key (the key is made in its desktop app, which has no web address for it)
KEY_URL = 'https://docs.granola.ai/help-center/sharing/integrations/personal-api'
SETUP = {
    'label': 'Granola',
    'what': 'Meeting notes and transcripts from Granola.',
    'account': {'id': 'granola', 'service': 'granola', 'transport': 'api', 'boundary': 'work', 'credential': 'granola',
                'poll_seconds': 900},
    'secret': 'Granola API key',
    'token_url': KEY_URL,
    'note': 'In Granola: Settings, Connectors, API keys. Needs a Business or Enterprise plan. Only reads.',
    'hints': {'granola_key_rejected': 'Granola asks for a new API key',
              'granola_http:HTTP_403': 'Granola refused: API keys need a Business or Enterprise plan'},
    # What the owner reads when the check turns the key down (onboarding.connect): plain words and what to do.
    'errors': {'granola_key_rejected': ('Granola didn’t accept that key', 'create a new one in Granola and paste it here'),
               'granola_http:HTTP_403': ('Granola didn’t allow that key', 'API keys need a Business or Enterprise plan'),
               'granola_credential_unavailable': ('That doesn’t look like a Granola API key', 'copy it again from Granola and paste it here'),
               'granola_network': ('Granola didn’t answer', 'try again in a minute')},
}
BASE = 'https://public-api.granola.ai'
NOTE_ID = r'not_[A-Za-z0-9]{14}'
PAGE = 30            # Granola's most notes per page
PAGES = 20           # at most 600 notes listed per run
TRANSCRIPT_PAGE = 100
TRANSCRIPT_PAGES = 60  # at most 6,000 transcript items of one meeting
MAX_NOTES = 25       # per run, at most this many notes are read (the rest next run)
OVERLAP_HOURS = 2    # notes are written, and edited, a while after the meeting: reread a little back each time
SETTLE_HOURS = 48    # a note still without notes or transcript after this long is passed, not asked for again
GAP = 0.25           # seconds between requests: 4 a second, under Granola's 5
NOTES_CHARS = 40_000
TRANSCRIPT_CHARS = 400_000  # a long meeting's whole transcript, as from Zoom
SEEN_KEEP = 1000
TOKEN = re.compile(r'[\x21-\x7e]{8,4000}')  # opaque: any printable text without spaces
_last = [0.0]


def stamp(value):
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    except (TypeError, ValueError):
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)


def zulu(moment):
    return moment.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def clean(value):
    return str(value or '').strip().lower()


def plain(value):
    """Text as given, without explicitly labeled passwords or one-time codes."""
    return re.sub(r'(?i)\b(password|passcode|one[- ]time code|verification code|otp)\s*[:=]\s*\S+', r'\1: [omitted]', str(value or ''))


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # never forward the key to a redirect target


class Source:
    def __init__(self, config, account, helpers):
        self.config, self.account, self.helpers = config, account, helpers
        try:
            secret = helpers.credential(config, account.get('credential') or 'granola')
        except Exception:
            raise helpers.SourceError('granola_credential_unavailable') from None
        secret = str(secret or '').strip()
        if not TOKEN.fullmatch(secret):
            raise helpers.SourceError('granola_credential_unavailable')
        self.headers = {'Authorization': 'Bearer ' + secret, 'Accept': 'application/json', 'User-Agent': 'TheMachine/1'}
        self.opener = urllib.request.build_opener(NoRedirect())
        self.owners = []  # the owner address of each note listed (whose())

    def get(self, path, params=None):
        """One GET to Granola's API: the notes list, one note, or one note's transcript. Never any other method,
        endpoint or host."""
        if not (path == '/v1/notes' or re.fullmatch(r'/v1/notes/' + NOTE_ID + r'(?:/transcript)?', path)):
            raise self.helpers.SourceError('granola_path_not_allowed')
        wait = _last[0] + GAP - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.monotonic()
        request = urllib.request.Request(BASE + path + ('?' + urllib.parse.urlencode(params) if params else ''),
                                         headers=self.headers, method='GET')
        try:
            with self.opener.open(request, timeout=30) as response:
                body = response.read(20_000_001)
            if len(body) > 20_000_000:
                raise self.helpers.SourceError('granola_response_too_large')
            return json.loads(body or b'{}')
        except urllib.error.HTTPError as error:
            retry = error.headers.get('Retry-After', '') if error.headers else ''
            error.close()
            if error.code == 401:
                raise self.helpers.SourceError('granola_key_rejected', 401) from None
            delay = min(3600, max(1, int(retry))) if retry.isdigit() else (60 if error.code == 429 else None)
            raise self.helpers.SourceError('granola_http', error.code, retry_after=delay) from None
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException):
            raise self.helpers.SourceError('granola_network') from None
        except (ValueError, UnicodeError):
            raise self.helpers.SourceError('granola_invalid_json') from None

    def listed(self, since):
        """[(note id, updated_at, deleted)] of the notes updated after `since`, as Granola lists them."""
        found, cursor = [], ''
        for _ in range(PAGES):
            params = {'updated_after': zulu(since), 'page_size': PAGE, **({'cursor': cursor} if cursor else {})}
            page = self.get('/v1/notes', params)
            if not isinstance(page, dict) or not isinstance(page.get('notes'), list):
                raise self.helpers.SourceError('granola_invalid_page')
            self.owners += [clean(item['owner'].get('email')) for item in page['notes'] if isinstance(item, dict) and isinstance(item.get('owner'), dict)]
            for item in page['notes']:
                if isinstance(item, dict) and isinstance(item.get('id'), str) and re.fullmatch(NOTE_ID, item['id']):
                    found.append((item['id'], str(item.get('updated_at') or ''), bool(item.get('deleted_at'))))
            next_cursor = page.get('cursor') if page.get('hasMore') else None
            if not next_cursor:
                return found, False
            if not isinstance(next_cursor, str) or next_cursor == cursor:
                raise self.helpers.SourceError('granola_invalid_cursor')
            cursor = next_cursor
        return found, True

    def note(self, note_id):
        """One note with its transcript inline, or with the transcript read in pages when it is too large for that.
        None when it is gone or no longer this key's to read."""
        try:
            return self.get(f'/v1/notes/{note_id}', {'include': 'transcript'})
        except self.helpers.SourceError as error:
            if error.status == 404:
                return None
            if error.status != 413:
                raise
        found = self.get(f'/v1/notes/{note_id}')
        if isinstance(found, dict):
            found['transcript'] = self.transcript(note_id)
        return found

    def transcript(self, note_id):
        """A long meeting's transcript items, page by page; None when Granola won't give it (an admin turned it off)."""
        items, cursor = [], ''
        try:
            for _ in range(TRANSCRIPT_PAGES):
                page = self.get(f'/v1/notes/{note_id}/transcript', {'page_size': TRANSCRIPT_PAGE, **({'cursor': cursor} if cursor else {})})
                if not isinstance(page, dict) or not isinstance(page.get('transcript'), list):
                    raise self.helpers.SourceError('granola_invalid_transcript')
                items += page['transcript']
                cursor = page.get('cursor') if page.get('hasMore') else None
                if not cursor or not isinstance(cursor, str):
                    break
        except self.helpers.SourceError as error:
            if error.status in (403, 404):
                return None
            raise
        return items


def whose(owners, known):
    """The key's own address from the owners of the notes it lists: one of the owner's known addresses, else the one
    that owns most of them (a personal key lists its own notes and the few shared with it). '' when it lists none."""
    owners = [a for a in owners if '@' in a]
    return next((a for a in owners if a in known), '') or max(sorted(set(owners)), key=owners.count, default='')


def owner_addresses(config, account):
    """The owner's own addresses: Granola's, their mailboxes and calendars, and config owner_emails."""
    found = {clean(account.get('email'))}
    try:
        import own_addresses
        found |= set(own_addresses.primaries(config)) | own_addresses.configured(config)[0]
    except Exception:  # noqa: BLE001 - Granola's own address is enough on its own
        pass
    return found - {''}


def speaker(item, owner_name):
    """Who said a transcript line: the identified name, the note-taker for "me", else Granola's label."""
    who = item.get('speaker') if isinstance(item.get('speaker'), dict) else {}
    name = ' '.join(str(who.get('name') or '').split())[:80]
    if name:
        return name
    if who.get('attribution') == 'me':
        return owner_name or 'Note-taker'
    return ' '.join(str(who.get('diarization_label') or '').split())[:80] or ('Others' if who.get('attribution') == 'them' else 'Speaker')


def transcript_text(items, owner_name):
    """Transcript items as 'Speaker: words' lines, a speaker's run joined."""
    lines, last = [], None
    for item in items or ():
        if not isinstance(item, dict):
            continue
        text = ' '.join(str(item.get('text') or '').split())
        if not text:
            continue
        who = speaker(item, owner_name)
        if who == last and lines:
            lines[-1] += ' ' + text
        else:
            lines.append(f'{who}: {text}')
            last = who
    return plain('\n'.join(lines))


def notes_text(found):
    """The note as Markdown: Granola's summary, then the owner's own notes when the key may read them."""
    summary = found.get('summary_markdown') or found.get('summary_text') or ''
    private = found.get('private_notes_markdown') or found.get('private_notes_text') or ''
    parts = [str(summary).strip()] if str(summary).strip() else []
    if str(private).strip():
        parts.append('## My notes\n\n' + str(private).strip())
    return plain('\n\n'.join(parts))


def people(found):
    """[{email, name}] of the meeting: its attendees, then calendar invitees not among them (at most 200)."""
    out, seen = [], set()
    event = found.get('calendar_event') if isinstance(found.get('calendar_event'), dict) else {}
    for person in list(found.get('attendees') or ()) + list(event.get('invitees') or ()):
        if not isinstance(person, dict):
            continue
        email = clean(person.get('email'))
        if '@' not in email or email in seen:
            continue
        seen.add(email)
        name = ' '.join(str(person.get('name') or '').split())[:120]
        out.append({'email': email, **({'name': name} if name else {})})
    return out[:200]


def source_id(kind, note_id):
    return kind + ':' + hashlib.sha256(note_id.encode()).hexdigest()[:32]


def events_for(account, found, mine, helpers):
    """The note's two signals: its notes and its transcript (each only when it has one). [] for a note of a meeting
    the owner was not in."""
    note_id = str(found.get('id') or '')
    if not re.fullmatch(NOTE_ID, note_id):
        raise helpers.SourceError('granola_invalid_note')
    event = found.get('calendar_event') if isinstance(found.get('calendar_event'), dict) else {}
    owner = found.get('owner') if isinstance(found.get('owner'), dict) else {}
    owner_email = clean(owner.get('email'))
    attendees = people(found)
    organizer = clean(event.get('organiser'))
    if owner_email not in mine and not any(p['email'] in mine for p in attendees) and organizer not in mine:
        return []  # shared with them, from a meeting they were not in
    items = found.get('transcript') if isinstance(found.get('transcript'), list) else []
    begun = stamp(event.get('scheduled_start_time')) or stamp(items[0].get('start_time') if items and isinstance(items[0], dict) else None) \
        or stamp(found.get('created_at'))
    if not begun:
        raise helpers.SourceError('granola_invalid_note')
    ended = stamp(event.get('scheduled_end_time')) or stamp(items[-1].get('end_time') if items and isinstance(items[-1], dict) else None)
    title = ' '.join(str(found.get('title') or event.get('event_title') or '').split()) or 'Meeting notes · ' + begun.date().isoformat()
    link = found.get('web_url')
    host = urllib.parse.urlsplit(link) if isinstance(link, str) else None
    owner_name = ' '.join(str(owner.get('name') or '').split())[:80]
    meta = {'note_id': note_id, 'start_at': begun.isoformat(), 'end_at': ended.isoformat() if ended and ended > begun else None,
            'host_email': organizer or owner_email,
            **({'calendar_event_id': str(event['calendar_event_id'])[:300]} if event.get('calendar_event_id') else {}),
            'owner_email': owner_email, 'from_me': owner_email in mine, 'attendees': attendees,
            'participants': [p.get('name') or p['email'] for p in attendees][:50],
            'edited_at': str(found.get('updated_at') or ''),
            **({'source_url': link} if host and host.scheme == 'https' and (host.hostname == 'granola.ai' or str(host.hostname).endswith('.granola.ai')) else {})}
    out = []
    body = notes_text(found)
    if body:
        out.append({'account_id': account['id'], 'source_id': source_id('notes', note_id), 'kind': 'granola.notes',
                    'occurred_at': begun.isoformat(), 'title': title[:1000], 'body': body[:NOTES_CHARS],
                    'metadata': {**meta, 'truncated': len(body) > NOTES_CHARS}, 'deleted': False})
    spoken = transcript_text(items, owner_name)
    if spoken:
        out.append({'account_id': account['id'], 'source_id': source_id('transcript', note_id), 'kind': 'granola.transcript',
                    'occurred_at': begun.isoformat(), 'title': title[:1000], 'body': spoken[:TRANSCRIPT_CHARS],
                    'metadata': {**{k: v for k, v in meta.items() if k not in ('participants',)}, 'truncated': len(spoken) > TRANSCRIPT_CHARS},
                    'deleted': False})
    return out


def gone(account, note_id, now):
    """A note deleted in Granola: both its signals go too."""
    return [{'account_id': account['id'], 'source_id': source_id(kind, note_id), 'kind': 'granola.' + kind, 'occurred_at': now.isoformat(),
             'title': '', 'body': '', 'metadata': {}, 'deleted': True} for kind in ('notes', 'transcript')]


def sync(store, config, account, helpers):
    source = Source(config, account, helpers)
    state = dict(store.checkpoint(account['id']) or {})
    now = stamp(helpers.now())
    since = stamp(state.get('since'))
    start = since - dt.timedelta(hours=OVERLAP_HOURS) if since else now - dt.timedelta(days=int(config.get('bootstrap_days', 7)))
    listed, cut = source.listed(start)
    mine = owner_addresses(config, account)
    mine |= {whose(source.owners, mine)} - {''}
    seen = dict(state.get('seen') or {})
    skipped = helpers.Skips('granola_invalid_note')
    count = read = waiting = 0
    todo = [x for x in listed if seen.get(x[0]) != x[1]]
    for note_id, edited, deleted in todo[:MAX_NOTES]:
        if deleted:
            events = gone(account, note_id, now) if note_id in seen else []
        else:
            found = source.note(note_id)
            read += 1
            if not isinstance(found, dict):
                events = gone(account, note_id, now) if note_id in seen else []
            else:
                events = skipped.take(events_for, account, found, mine, helpers)
                events = [] if events is skipped.SKIPPED else events
                made = stamp(found.get('created_at'))
                if not events and found.get('summary_markdown') is None and not found.get('transcript') and made \
                        and now - made < dt.timedelta(hours=SETTLE_HOURS):
                    waiting += 1  # Granola is still writing it: read it again next run
                    continue
        seen[note_id] = edited or 'read'
        if len(seen) > SEEN_KEEP:
            seen = dict(list(seen.items())[-SEEN_KEEP:])
        store.commit_page(account['id'], {**state, 'seen': seen}, events)
        count += len(events)
    skipped.check().note(state)
    more = cut or len(todo) > MAX_NOTES
    state.update(seen=seen, mode='incremental', coverage_complete=not more,
                 coverage='Older Granola notes are still being read.' if more else 'Granola notes caught up.')
    if not more and not waiting:
        state['since'] = now.isoformat()
    store.commit_page(account['id'], state, [])
    return {'mode': 'incremental', 'events': count, 'read': read, 'more': more, 'skipped': sum(skipped.values())}


def check(config, account, helpers):
    """A real read without storing anything: the key lists notes. It learns the key's address from them (the account is
    saved after this, onboarding.connect), so the card reads as that address."""
    source = Source(config, account, helpers)
    page = source.get('/v1/notes', {'page_size': PAGE})
    notes = page.get('notes') if isinstance(page, dict) and isinstance(page.get('notes'), list) else []
    found = whose([clean(n['owner'].get('email')) for n in notes if isinstance(n, dict) and isinstance(n.get('owner'), dict)],
                  owner_addresses(config, account))
    if found and '@' not in clean(account.get('email')):
        account['email'] = found
    return None
