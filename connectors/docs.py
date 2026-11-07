"""Documents as a connection: Google Docs and Drive, or Word on OneDrive and SharePoint.

What comes in (each an event, linked to people like mail): a doc someone shared with the owner (docs.shared), a comment
or reply on a doc the owner owns or a thread they are in (docs.comment), a comment anywhere that @mentions them
(docs.mention), and new suggested edits on a doc they own (docs.suggestion; tracked changes in Word).

The sign-in is the one the Machine already has for that address: Google through its token broker (google_api.py), and
Microsoft through its broker or the owner's own app (ms_graph.py). Gmail's and gog's scopes stay as they are. Reading
documents needs one more scope, which the owner grants with its own consent (Connect Google Docs, or Connect Microsoft
documents), and nothing else asks for it. Microsoft documents need no Outlook: without one on that address, the Docs
connection has a sign-in of its own (`own_grant`, onboarding.connect_docs_grant), with only the Docs scopes, which the
Outlook mail and calendar connectors never use:

- Google: https://www.googleapis.com/auth/drive.readonly (Drive file list, comments, a doc's text and its suggestions).
  Posting an owner-approved reply to a comment needs https://www.googleapis.com/auth/drive, a second, separate consent;
  without it a reply stays a draft to post by hand.
- Microsoft: Files.ReadWrite.All, asked in the one Docs consent (it also reads: the owner's OneDrive, and files shared
  with them on OneDrive and SharePoint); a connection from before reads with Files.Read.All only, until Allow edits.
  Microsoft Graph has no way to reply to a Word comment, so a reply there is always a draft to post by hand.

Abilities (abilities.py): Brings in signals is the sync above. Can do things is the rest: find a doc and read its text
when a to-do needs it (find, read_text), and the writes below. Without Brings in signals it is action-only: nothing is
synced, and refresh only checks what it may do. Google, without drive.readonly (a restricted scope), works with two
narrow ones instead: documents.readonly reads a Google Doc by its id (a link in a to-do's messages, or one found), and
drive.file makes a new doc and finds, syncs and reads the docs this app made. Gmail's and gog's scopes never change.

Writes, each only after the owner's OK on exactly that: drive.replies.create through Replier, for an approved doc_reply
(next_actions.py), and a new doc or a pinned edit through Writer, for an approved doc_write (doc_writes.py). Writing docs
needs Google's drive scope (the same one as replies; a new doc also works with drive.file), and Microsoft's
Files.ReadWrite.All, which comes with connecting Microsoft OneDrive (Allow edits only for a connection from before).
"""
import datetime as dt
import hashlib
import http.client
import io
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from xml.etree import ElementTree
from xml.parsers import expat

KINDS = {'docs.comment': 'Doc comment', 'docs.mention': 'Doc mention', 'docs.suggestion': 'Suggested edit',
         'docs.shared': 'Shared doc'}
SETUP = {
    # Microsoft only for now, so the tile says so; a Google Docs one gets its own name once the broker offers it
    'label': 'Microsoft OneDrive',
    'account': {'id': 'docs', 'service': 'docs', 'transport': 'broker', 'boundary': 'work', 'poll_seconds': 900},
    # Word files only for now, hosted and self-hosted alike: Google Docs come through the token broker, which doesn't
    # offer their consent yet (docs/help/docs.md)
    'what': 'Word files: comments, shares, and new docs or edits you approve.',
    'note': 'Signs in with Microsoft for that address, with or without Outlook. Press Connect documents on your setup '
            'page, or Sign in with Microsoft here.',
    'ask': [('email', 'The Microsoft address that owns the files')],
    # a hosted Machine: its account page's Docs tile has the consent (Connect documents); on a paired self-hosted one,
    # + Add signs in with Microsoft through the control plane (fleet.SIGNIN_OF, onboarding.connect_docs_grant)
    'account_page': 'docs',
    'hints': {'docs_not_connected': 'Press Connect Microsoft documents to let it read Word files',
              'docs_no_signin': 'Sign in with Microsoft for this address',
              'docs_signin_expired': 'Sign in again for this address'}}
READ_SCOPE = 'https://www.googleapis.com/auth/drive.readonly'
REPLY_SCOPE = 'https://www.googleapis.com/auth/drive'
MS_SCOPE = 'Files.Read.All'
DOCS_READ_SCOPE = 'https://www.googleapis.com/auth/documents.readonly'  # a Google Doc's text by its id (not restricted)
DOCS_SCOPE = 'https://www.googleapis.com/auth/documents'  # a Google Doc by its id, and an owner-approved edit to it (not restricted)
GOOGLE_DOCS = 'google_docs'  # Google Docs with its own sign-in and broker (google_docs_broker): documents and drive.file only
DOC_LINK = re.compile(r'https://docs\.google\.com/document/d/([A-Za-z0-9_-]{20,100})')
MAX_FOUND = 10
FILE_SCOPE = 'https://www.googleapis.com/auth/drive.file'  # Google: only files this app created (a new doc)
WRITE_KEY = 'themachine_write'  # a new Google Doc's appProperties key: the write's token, to find it again
MS_WRITE_SCOPE = 'Files.ReadWrite.All'
DOCX_MIME = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
DOC_MIME = 'application/vnd.google-apps.document'
EXPORT = {DOC_MIME: 'text/plain', 'application/vnd.google-apps.presentation': 'text/plain',
          'application/vnd.google-apps.spreadsheet': 'text/csv'}
WORD = ('.docx', '.docm')
LOOKBACK_DAYS = 30   # docs changed this recently are checked for new comments
OVERLAP_HOURS = 2    # each run rereads comments this far back, so one made during the last run is not missed
MAX_FILES = 40       # docs checked per run, most recently changed first
MAX_SHARED = 25
MAX_DOWNLOAD = 15_000_000
MAX_TEXT = 200_000   # characters of a doc's text handed to a run
SEEN_KEEP = 2000
DOWNLOAD_HOSTS = ('.sharepoint.com', '.1drv.com', '.livefilestore.com', '.onedrive.com', '.sharepoint.us', '.sharepoint.de')
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'


def provider(config, account):
    """google or microsoft: as set, else the provider of the owner's mail or calendar sign-in on this address."""
    if account.get('provider') in ('google', 'microsoft'):
        return account['provider']
    email = str(account.get('email') or '').lower()
    for a in config.get('accounts', []):
        if str(a.get('email') or '').lower() == email and a.get('service') in ('outlook', 'outlook_calendar'):
            return 'microsoft'
    return 'google'


def signin(config, account, helpers):
    """The sign-in to call with: the docs account itself, carrying the transport and credential of the owner's own Google
    or Microsoft connection on the same address, or its own sign-in (own_grant: Microsoft documents without Outlook,
    kept under the same address in mail_grants.py). Never one from a Fleet grant (someone else's)."""
    email = str(account.get('email') or '').strip().lower()
    if not email:
        raise helpers.SourceError('docs_no_email')
    kind = provider(config, account)
    if kind == 'google' and account.get('own_grant') and account.get('transport') == 'broker':
        # its own Google sign-in (a hosted Machine's Connect Google Docs), never Gmail's: kept as provider google_docs
        return {'id': account['id'], 'email': email, 'transport': 'broker', 'provider': GOOGLE_DOCS,
                **{k: account[k] for k in ('connected_at',) if account.get(k)}}
    if kind == 'microsoft' and account.get('own_grant') and account.get('transport') == 'broker':
        return {'id': account['id'], 'email': email, 'transport': 'broker',
                **{k: account[k] for k in ('connected_at',) if account.get(k)}}
    services = ('outlook', 'outlook_calendar') if kind == 'microsoft' else ('gmail', 'calendar')
    found = next((a for a in config.get('accounts', []) if a.get('service') in services and not a.get('shared')
                  and str(a.get('email') or '').lower() == email and a.get('transport') in ('broker', 'graph')), None)
    transport = account.get('transport') if account.get('transport') in ('broker', 'graph') else None
    if not found and not transport:
        raise helpers.SourceError('docs_no_signin')
    base = found or account
    if kind == 'google' and base.get('transport') != 'broker':
        raise helpers.SourceError('docs_no_signin')  # gog's own sign-in keeps its scopes: Google Docs come through the broker
    return {'id': account['id'], 'email': email, 'transport': base.get('transport'),
            **{k: base[k] for k in ('credential', 'connected_at') if base.get(k)}}


def google_scopes(config, helpers, sign):
    """The scopes the owner granted this Google sign-in, at its own broker (Gmail's, or Google Docs' own)."""
    import google_api  # noqa: PLC0415
    return set(google_api.scopes(config, helpers.credential, sign, provider=sign.get('provider') or 'google'))


class Google:
    def __init__(self, config, account, helpers):
        import google_api
        self.api, self.config, self.account, self.helpers = google_api, config, account, helpers
        self.signin = signin(config, account, helpers)

    def granted(self):
        """The scopes this sign-in has (asked once; unknown: none)."""
        if not hasattr(self, '_granted'):
            try:
                self._granted = google_scopes(self.config, self.helpers, self.signin)
            except Exception:  # noqa: BLE001 - unknown: the call itself says what is missing
                self._granted = set()
        return self._granted

    def read_scope(self):
        """drive.readonly when granted (every doc), else drive.file (the docs this app made), else drive.readonly, whose
        refusal says Connect Google Docs."""
        granted = self.granted()
        return READ_SCOPE if READ_SCOPE in granted or FILE_SCOPE not in granted else FILE_SCOPE

    def call(self, method, params, scope=None, raw=False, limit=None, body=None, write=False, content_type=None):
        scope = scope or self.read_scope()
        try:
            return self.api.call(self.config, self.helpers.credential, self.signin, method, params, scope, body=body,
                                 write=write, raw=raw, limit=limit, provider=self.signin.get('provider') or 'google',
                                 **({'content_type': content_type} if content_type else {}))
        except self.api.BrokerError as error:
            if error.category == 'google_scope_not_granted':
                raise self.helpers.SourceError('docs_not_connected', error.status) from None
            if error.status == 401:
                raise self.helpers.SourceError('docs_signin_expired', 401) from None
            failure = self.helpers.SourceError('docs_' + str(error.category), error.status,
                                               retry_after=getattr(error, 'retry_after', None) or (60 if error.status == 429 else None))
            failure.reason = getattr(error, 'reason', None)
            raise failure from None

    def me(self):
        about = self.call('drive.about.get', {'fields': 'user(displayName,emailAddress)'})
        return (about.get('user') or {}) if isinstance(about, dict) else {}

    def files(self, query, order, limit, fields):
        found, token = [], ''
        while len(found) < limit:
            params = {'q': query, 'orderBy': order, 'pageSize': min(100, limit), 'spaces': 'drive',
                      'includeItemsFromAllDrives': True, 'supportsAllDrives': True, 'corpora': 'allDrives',
                      'fields': 'nextPageToken,incompleteSearch,files(' + fields + ')'}
            if token:
                params['pageToken'] = token
            page = self.call('drive.files.list', params)
            found += [f for f in page.get('files') or [] if isinstance(f, dict) and f.get('id')]
            token = page.get('nextPageToken') or ''
            if not token:
                break
        return found[:limit]

    def files_page(self, query, order, limit, fields, token=None):
        params = {'q': query, 'orderBy': order, 'pageSize': limit, 'spaces': 'drive',
                  'includeItemsFromAllDrives': True, 'supportsAllDrives': True, 'corpora': 'allDrives',
                  'fields': 'nextPageToken,incompleteSearch,files(' + fields + ')'}
        if token:
            params['pageToken'] = token
        page = self.call('drive.files.list', params)
        if page.get('incompleteSearch'):
            raise self.helpers.SourceError('docs_incomplete_search')
        return [f for f in page.get('files') or [] if isinstance(f, dict) and f.get('id')], page.get('nextPageToken')

    def comments(self, file_id, since):
        found, token = [], ''
        for _ in range(10):
            params = {'startModifiedTime': zulu(since), 'pageSize': 100, 'includeDeleted': False,
                      'fields': 'nextPageToken,comments(id,author(displayName,emailAddress,me),content,htmlContent,'
                                'quotedFileContent(value),createdTime,modifiedTime,resolved,deleted,'
                                'replies(id,author(displayName,emailAddress,me),content,htmlContent,createdTime,modifiedTime,deleted,action))'}
            if token:
                params['pageToken'] = token
            try:
                page = self.call('drive.comments.list', {'fileId': file_id, **params})
            except self.helpers.SourceError as error:
                if error.status in (403, 404):
                    return found  # comments closed to this sign-in, or the file is gone
                raise
            found += [c for c in page.get('comments') or [] if isinstance(c, dict) and c.get('id')]
            token = page.get('nextPageToken') or ''
            if not token:
                break
        return found

    def suggestions(self, file_id):
        """{suggestion id: the text it inserts or deletes} in a Google Doc."""
        try:
            doc = self.call('docs.documents.get', {'documentId': file_id, 'suggestionsViewMode': 'SUGGESTIONS_INLINE'})
        except self.helpers.SourceError as error:
            if error.status in (400, 403, 404):
                return {}
            raise
        return doc_suggestions(doc)

    def text(self, file_id):
        if self.read_scope() != READ_SCOPE and self.granted() & {DOCS_READ_SCOPE, DOCS_SCOPE}:
            return self.doc_text(file_id)  # no drive.readonly: a Google Doc by its id, with documents(.readonly)
        info = self.call('drive.files.get', {'fileId': file_id, 'fields': 'id,name,mimeType,webViewLink', 'supportsAllDrives': True})
        mime = EXPORT.get(info.get('mimeType'))
        if not mime:
            raise self.helpers.SourceError('docs_text_unsupported')
        data = self.call('drive.files.export', {'fileId': file_id, 'mimeType': mime}, raw=True, limit=MAX_DOWNLOAD)
        return info, data.decode('utf-8', 'replace')


    def doc_text(self, file_id):
        """A Google Doc's title, link and text through the Docs API (documents.readonly): Google Docs only."""
        try:
            doc = self.call('docs.documents.get', {'documentId': file_id}, scope=self.docs_scope())
        except self.helpers.SourceError as error:
            if error.status in (400, 404):
                raise self.helpers.SourceError('docs_text_unsupported', error.status) from None
            raise
        import doc_writes  # noqa: PLC0415
        text = '\n'.join(p['text'] for p in doc_writes.google_paragraphs(doc))
        return {'name': doc.get('title'), 'webViewLink': doc_writes.google_link(file_id)}, text

    def docs_scope(self):
        """The Docs API scope for a doc by its id: documents.readonly when granted (reads only), else documents."""
        return DOCS_READ_SCOPE if DOCS_READ_SCOPE in self.granted() or DOCS_SCOPE not in self.granted() else DOCS_SCOPE

    def find(self, words):
        """Docs matching these words: Drive's full-text search with drive.readonly, else among the docs this app made
        (drive.file), by name."""
        quoted = words.replace('\\', '\\\\').replace("'", "\\'")
        wide = self.read_scope() == READ_SCOPE
        query = f"trashed = false and {'fullText' if wide else 'name'} contains '{quoted}'"
        found = self.files(query, '' if wide else 'modifiedTime desc', MAX_FOUND, 'id,name,mimeType,webViewLink,modifiedTime')
        return [{'file_id': f['id'], 'title': f.get('name') or '', 'url': f.get('webViewLink'), 'at': f.get('modifiedTime')}
                for f in found if f.get('mimeType') in EXPORT]


class Microsoft:
    def __init__(self, config, account, helpers):
        import ms_graph
        self.api, self.config, self.account, self.helpers = ms_graph, config, account, helpers
        self.signin = signin(config, account, helpers)

    def call(self, method, params=None, **write):
        try:
            return self.api.call(self.config, self.helpers.credential, self.signin, method, params, **write)
        except self.api.GraphError as error:
            if error.category == 'microsoft_scope_not_granted' or error.status == 403:
                raise self.helpers.SourceError('docs_not_connected', error.status) from None
            if 'signin_expired' in error.category or error.status == 401:
                raise self.helpers.SourceError('docs_signin_expired', error.status, retry_after=3600) from None
            raise self.helpers.SourceError('docs_microsoft', error.status, retry_after=error.retry_after) from None

    def me(self):
        drive = self.call('drive.get', {'$select': 'id,owner'})
        user = ((drive.get('owner') or {}).get('user') or {}) if isinstance(drive, dict) else {}
        return {'displayName': user.get('displayName'), 'emailAddress': user.get('email'), 'drive': drive.get('id')}

    def delta(self, token):
        """Changed items in the owner's own drive since `token` (None: just a starting point), and the next token."""
        items, params = [], ({'token': token} if token else {'token': 'latest'})
        for _ in range(20):
            page = self.call('drive.delta', params)
            items += [i for i in page.get('value') or [] if isinstance(i, dict)]
            link = page.get('@odata.nextLink')
            if link:
                params = {'token': link_token(link)}
                continue
            return (items if token else []), link_token(page.get('@odata.deltaLink') or '')
        return items, link_token(page.get('@odata.nextLink') or '')

    def shared(self):
        page = self.call('drive.shared', {'$top': 100})
        return [i for i in page.get('value') or [] if isinstance(i, dict)]

    def item(self, drive, item_id):
        return self.call('drives.item', {'drive': drive, 'id': item_id})

    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        """A download link that redirects is refused: it could point away from Microsoft's hosts."""
        def redirect_request(self, *args, **kwargs):
            return None

    def download(self, item):
        """A file's bytes from its pre-signed download link (Microsoft's own file hosts only, no token sent along)."""
        link = str(item.get('@microsoft.graph.downloadUrl') or '')
        host = urllib.parse.urlsplit(link)
        if host.scheme != 'https' or not str(host.hostname or '').endswith(DOWNLOAD_HOSTS):
            raise self.helpers.SourceError('docs_unexpected_host')
        if int(item.get('size') or 0) > MAX_DOWNLOAD:
            raise self.helpers.SourceError('docs_file_too_large')
        try:
            with urllib.request.build_opener(self._NoRedirect).open(urllib.request.Request(link, method='GET'), timeout=60) as response:
                data = response.read(MAX_DOWNLOAD + 1)
        except urllib.error.HTTPError as error:
            error.close()
            raise self.helpers.SourceError('docs_download', error.code) from None
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException):
            raise self.helpers.SourceError('docs_network') from None
        if len(data) > MAX_DOWNLOAD:
            raise self.helpers.SourceError('docs_file_too_large')
        return data

    def find(self, words):
        """Word, text and Markdown files in the owner's OneDrive that match these words (Graph's drive search)."""
        page = self.call('drive.search', {'q': words, '$top': 50})
        out = []
        for item in page.get('value') or []:
            drive = str((item.get('parentReference') or {}).get('driveId') or '') if isinstance(item, dict) else ''
            if drive and item.get('id') and str(item.get('name') or '').lower().endswith(WORD + ('.txt', '.md')):
                out.append({'file_id': drive + '!' + str(item['id']), 'title': item.get('name') or '', 'url': item.get('webUrl'),
                            'at': item.get('lastModifiedDateTime')})
        return out[:MAX_FOUND]

    def text(self, file_id):
        drive, _, item_id = str(file_id).partition('!')
        item = self.item(drive, item_id)
        name = str(item.get('name') or '')
        data = self.download(item)
        if name.lower().endswith(WORD):
            return item, word_text(data)
        if name.lower().endswith(('.txt', '.md', '.csv')):
            return item, data.decode('utf-8', 'replace')
        raise self.helpers.SourceError('docs_text_unsupported')


def source_for(config, account, helpers):
    return (Microsoft if provider(config, account) == 'microsoft' else Google)(config, account, helpers)


# ------------------------------------------------------------------------------------------- parsing

def zulu(moment):
    return moment.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')


def stamp(value):
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    except (TypeError, ValueError):
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)


def link_token(link):
    """The token of a Graph delta or next link (?token=… or (token='…'))."""
    found = re.search(r"token=(?:'([^']+)'|([^&)]+))", urllib.parse.unquote(str(link or '')))
    return (found[1] or found[2]) if found else ''


def short_id(*parts):
    return hashlib.sha256('\x00'.join(str(p) for p in parts).encode()).hexdigest()[:32]


def person(user):
    """(name, address) of a Drive or Graph user; the address only when the source shows it."""
    user = user if isinstance(user, dict) else {}
    name = ' '.join(str(user.get('displayName') or '').split())[:120]
    email = str(user.get('emailAddress') or user.get('email') or '').strip().lower()
    return name, (email if re.fullmatch(r'[^@\s<>]{1,64}@[^@\s<>]{1,253}', email) else '')


def sender(name, email):
    return f'{name} <{email}>' if name and email else email or name


def plain(text):
    return ' '.join(re.sub(r'<[^>]+>', ' ', str(text or '')).split())


def mentions(owner, comment):
    """Whether the comment (or its HTML) @mentions the owner's address."""
    text = (str(comment.get('content') or '') + ' ' + str(comment.get('htmlContent') or '')).lower()
    return bool(owner) and (('@' + owner) in text or ('+' + owner) in text or ('mailto:' + owner) in text)


def doc_suggestions(doc):
    """{suggestion id: inserted or deleted text} from a Docs API document read with SUGGESTIONS_INLINE."""
    found = {}

    def walk(node):
        if isinstance(node, dict):
            run = node.get('textRun')
            if isinstance(run, dict):
                for key, verb in (('suggestedInsertionIds', 'Add'), ('suggestedDeletionIds', 'Remove')):
                    for sid in run.get(key) or []:
                        text = ' '.join(str(run.get('content') or '').split())
                        found[str(sid)] = (found.get(str(sid), '') + ' ' + text).strip() if str(sid) in found else f'{verb}: {text}'
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)
    walk(doc.get('body') or {})
    walk(doc.get('tabs') or [])
    return {k: v[:300] for k, v in found.items()}


def parse_xml(raw):
    """ElementTree from bytes, refusing any DTD (so no entity expansion or external entities), as defusedxml does.
    A .docx comes from whoever shared it: untrusted. Same parser as connectors/rss.py."""
    builder = ElementTree.TreeBuilder()
    parser = expat.ParserCreate(namespace_separator='}')
    name = lambda tag: '{' + tag if '}' in tag else tag  # expat's 'ns}tag' as ElementTree's '{ns}tag'

    def refuse(*_):
        raise ElementTree.ParseError('XML with a DTD or entities is refused')
    parser.StartDoctypeDeclHandler = parser.EntityDeclHandler = parser.ExternalEntityRefHandler = refuse
    parser.StartElementHandler = lambda tag, attrs: builder.start(name(tag), {name(k): v for k, v in attrs.items()})
    parser.EndElementHandler = lambda tag: builder.end(name(tag))
    parser.CharacterDataHandler = builder.data
    parser.buffer_text = True
    try:
        parser.Parse(raw, True)
    except expat.ExpatError as error:
        raise ElementTree.ParseError(str(error)) from None
    return builder.close()


def _xml(data, name):
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as package:
            if name not in package.namelist():
                return None
            info = package.getinfo(name)
            if info.file_size > 50_000_000:
                return None
            return parse_xml(package.read(name))
    except (zipfile.BadZipFile, ElementTree.ParseError, KeyError, OSError, ValueError):
        return None


def _text(node):
    return ' '.join(''.join(t.text or '' for t in node.iter() if t.tag in (W + 't', W + 'delText')).split())


def word_text(data):
    """A .docx file's text, a paragraph per line."""
    root = _xml(data, 'word/document.xml')
    if root is None:
        return ''
    return '\n'.join(line for line in (_text(p) for p in root.iter(W + 'p')) if line)


def word_comments(data):
    """[{id, author, date, text, mailto}] of a .docx file's comments; mailto: the addresses its links point at
    (Word's @mentions)."""
    root = _xml(data, 'word/comments.xml')
    if root is None:
        return []
    rels = _xml(data, 'word/_rels/comments.xml.rels')
    targets = {r.get('Id'): str(r.get('Target') or '') for r in (rels if rels is not None else [])}
    out = []
    for c in root.iter(W + 'comment'):
        links = {targets.get(h.get(R + 'id'), '') for h in c.iter(W + 'hyperlink')}
        out.append({'id': c.get(W + 'id'), 'author': ' '.join(str(c.get(W + 'author') or '').split())[:120],
                    'date': c.get(W + 'date') or '', 'text': _text(c),
                    'mailto': {t[7:].split('?')[0].lower() for t in links if t.lower().startswith('mailto:')}})
    return out


def word_changes(data):
    """[{id, verb, author, date, text}] of a .docx file's tracked changes (Word's suggested edits)."""
    root = _xml(data, 'word/document.xml')
    if root is None:
        return []
    out = []
    for tag, verb in ((W + 'ins', 'Add'), (W + 'del', 'Remove')):
        for node in root.iter(tag):
            text = _text(node)
            if text:
                out.append({'id': f"{verb[0]}{node.get(W + 'id')}", 'verb': verb, 'author': str(node.get(W + 'author') or '')[:120],
                            'date': node.get(W + 'date') or '', 'text': text[:300]})
    return out


# ------------------------------------------------------------------------------------------- events

def event(account, kind, key, at, title, body, meta):
    return {'account_id': account['id'], 'source_id': kind.split('.')[1] + ':' + key, 'kind': kind, 'occurred_at': at,
            'title': ' '.join(str(title or 'Untitled document').split())[:1000], 'body': str(body or '')[:40000],
            'metadata': meta, 'deleted': False}


def google_comment_events(account, owner, info, comments, since, seen):
    """docs.comment and docs.mention events from one doc's comments: someone else's comment or reply on a doc the owner
    owns or a thread they are in, and any comment that @mentions them. Each (comment or reply, edit) once."""
    out = []
    owned = any(o.get('me') for o in info.get('owners') or [] if isinstance(o, dict))
    link = str(info.get('webViewLink') or '')
    for c in comments:
        if c.get('deleted'):
            continue
        thread = [c] + [r for r in c.get('replies') or [] if isinstance(r, dict) and not r.get('deleted')]
        mine_in = any((p.get('author') or {}).get('me') for p in thread)
        quoted = ' '.join(str((c.get('quotedFileContent') or {}).get('value') or '').split())[:500]
        for part in thread:
            author = part.get('author') or {}
            at = stamp(part.get('modifiedTime') or part.get('createdTime'))
            if author.get('me') or not at or at < since:
                continue
            mention = mentions(owner, part)
            if not (mention or owned or mine_in):
                continue
            key = short_id(info['id'], c['id'], part.get('id') if part is not c else '')
            edit = str(part.get('modifiedTime') or part.get('createdTime'))
            if seen.get(key) == edit:
                continue
            seen[key] = edit
            name, email = person(author)
            said = plain(part.get('content') or part.get('htmlContent'))
            earlier = [f"{person(p.get('author'))[0] or 'Someone'}: {plain(p.get('content'))}" for p in thread[:thread.index(part)]][-5:]
            body = (f'On: “{quoted}”\n\n' if quoted else '') + ('\n'.join(earlier) + '\n\n' if earlier else '') + f'{name or "Someone"}: {said}'
            url = link + ('&' if '?' in link else '?') + 'disco=' + urllib.parse.quote(c['id']) if link.startswith('https://') else ''
            out.append(event(account, 'docs.mention' if mention else 'docs.comment', key, at.isoformat(), info.get('name'), body, {
                'provider': 'google', 'file_id': info['id'], 'comment_id': c['id'], 'reply_id': part.get('id') if part is not c else None,
                'doc_title': info.get('name'), 'from': sender(name, email), 'from_name': name, 'to': owner, 'owned': owned,
                'mention': mention, 'resolved': bool(c.get('resolved')), 'mime': info.get('mimeType'),
                'quoted': quoted, **({'source_url': url} if url else {})}))
    return out


def shared_event(account, owner, provider_name, file_id, title, at, by, link, mime=None):
    name, email = by
    return event(account, 'docs.shared', short_id(file_id, 'shared'), at, title,
                 f'{name or email or "Someone"} shared “{title}” with you.',
                 {'provider': provider_name, 'file_id': file_id, 'doc_title': title, 'from': sender(name, email), 'from_name': name,
                  'to': owner, 'mime': mime, **({'source_url': link} if str(link or '').startswith('https://') else {})})


def suggestion_event(account, owner, provider_name, file_id, title, at, items, by, link):
    """New suggested edits on one doc the owner owns: one event per run that found some, listing them."""
    name, email = by
    lines = [f'- {t}' for t in items[:20]] + ([f'- and {len(items) - 20} more'] if len(items) > 20 else [])
    return event(account, 'docs.suggestion', short_id(file_id, 'suggestions', at, len(items)), at, title,
                 f'{len(items)} new suggested edit{"s" if len(items) != 1 else ""} on “{title}”'
                 + (f', by {name or email}' if name or email else '') + ':\n' + '\n'.join(lines),
                 {'provider': provider_name, 'file_id': file_id, 'doc_title': title, 'from': sender(name, email), 'from_name': name,
                  'to': owner, 'owned': True, 'count': len(items), **({'source_url': link} if str(link or '').startswith('https://') else {})})


def trim(seen):
    return dict(list(seen.items())[-SEEN_KEEP:]) if len(seen) > SEEN_KEEP else seen


def sync_google(store, config, account, helpers, state, now):
    source = Google(config, account, helpers)
    owner = str(account['email']).lower()
    since = stamp(state.get('since'))
    start = (since - dt.timedelta(hours=OVERLAP_HOURS)) if since else now - dt.timedelta(days=int(config.get('bootstrap_days', 7)))
    cycle = dict(state.get('google_cycle') or {'at': now.isoformat()})
    if since is None:
        start = stamp(cycle['at']) - dt.timedelta(days=int(config.get('bootstrap_days', 7)))
    window = zulu(stamp(cycle['at']) - dt.timedelta(days=LOOKBACK_DAYS))
    seen, marks = dict(state.get('seen') or {}), dict(state.get('suggested') or {})
    events = []
    fields = 'id,name,mimeType,webViewLink,modifiedTime,sharedWithMeTime,sharingUser(displayName,emailAddress,me),owners(displayName,emailAddress,me),lastModifyingUser(displayName,emailAddress,me)'
    shared, next_shared = ([], None) if cycle.get('shared_done') else source.files_page(
        "sharedWithMe = true and trashed = false", 'sharedWithMeTime desc', MAX_SHARED, fields, cycle.get('shared'))
    if next_shared and shared and (stamp(shared[-1].get('sharedWithMeTime')) or start) < start:
        next_shared = None  # newest share first: the next page is older still, past what this sync looks at
    cycle.update(shared=next_shared, shared_done=not next_shared)
    for f in shared:
        at = stamp(f.get('sharedWithMeTime'))
        key = short_id(f['id'], 'shared')
        if at and at >= start and key not in seen and not (f.get('sharingUser') or {}).get('me'):
            seen[key] = 'shared'
            events.append(shared_event(account, owner, 'google', f['id'], f.get('name'), at.isoformat(),
                                       person(f.get('sharingUser') or (f.get('owners') or [{}])[0]), f.get('webViewLink'), f.get('mimeType')))
    recent, next_recent = ([], None) if cycle.get('recent_done') else source.files_page(
        f"trashed = false and modifiedTime > '{window}' and ('me' in owners or sharedWithMe = true)",
        'modifiedTime desc', MAX_FILES, fields, cycle.get('recent'))
    cycle.update(recent=next_recent, recent_done=not next_recent)
    for f in recent:
        events += google_comment_events(account, owner, f, source.comments(f['id'], start), start, seen)
        owned = any(o.get('me') for o in f.get('owners') or [] if isinstance(o, dict))
        changed = stamp(f.get('modifiedTime'))
        if owned and f.get('mimeType') == DOC_MIME and changed and changed >= start:
            found = source.suggestions(f['id'])
            known = set(marks.get(f['id']) or [])
            new = [text for sid, text in found.items() if sid not in known]
            if found or f['id'] in marks:
                marks[f['id']] = sorted(found)[:500]
            editor = f.get('lastModifyingUser') or {}
            if new and since is not None and not editor.get('me'):  # the first run only learns what is already there
                events.append(suggestion_event(account, owner, 'google', f['id'], f.get('name'), changed.isoformat(), new,
                                               person(editor), f.get('webViewLink')))
    more = not (cycle['shared_done'] and cycle['recent_done'])
    return events, {'seen': trim(seen), 'suggested': dict(list(marks.items())[-200:]),
                    'google_cycle': cycle if more else None, 'more': more, 'caught_up_at': cycle['at']}


def sync_microsoft(store, config, account, helpers, state, now):
    source = Microsoft(config, account, helpers)
    owner = str(account['email']).lower()
    since = stamp(state.get('since'))
    start = (since - dt.timedelta(hours=OVERLAP_HOURS)) if since else now - dt.timedelta(days=int(config.get('bootstrap_days', 7)))
    seen, marks = dict(state.get('seen') or {}), dict(state.get('suggested') or {})
    events = []
    shared_docs = []
    for item in ([] if state.get('word_pending') else source.shared()[:MAX_SHARED * 2]):
        remote = item.get('remoteItem') if isinstance(item.get('remoteItem'), dict) else item
        share = (remote.get('shared') or {}) if isinstance(remote.get('shared'), dict) else {}
        drive = str((remote.get('parentReference') or {}).get('driveId') or '')
        if not remote.get('id') or not drive:
            continue
        file_id = drive + '!' + str(remote['id'])
        at = stamp(share.get('sharedDateTime'))
        key = short_id(file_id, 'shared')
        holder = share.get('sharedBy') or share.get('owner') or {}
        by = person(holder.get('user') if isinstance(holder, dict) else {})
        if at and at >= start and key not in seen and by[1] != owner:
            seen[key] = 'shared'
            events.append(shared_event(account, owner, 'microsoft', file_id, remote.get('name'), at.isoformat(), by, remote.get('webUrl'),
                                       (remote.get('file') or {}).get('mimeType')))
        changed = stamp(remote.get('lastModifiedDateTime'))
        if str(remote.get('name') or '').lower().endswith(WORD) and changed and changed >= start:
            shared_docs.append((drive, str(remote['id']), False))
    changes, token = ([], state.get('word_next')) if state.get('word_pending') else source.delta(state.get('delta'))
    own = [(str((i.get('parentReference') or {}).get('driveId') or ''), str(i['id']), True) for i in changes
           if i.get('id') and 'deleted' not in i and str(i.get('name') or '').lower().endswith(WORD)]
    pending = list(state.get('word_pending') or own + shared_docs)
    for drive, item_id, owned in pending[:MAX_FILES]:
        try:
            item = source.item(drive, item_id)
            data = source.download(item)
        except helpers.SourceError as error:
            if error.status in (403, 404, 423) or error.category in ('docs_file_too_large', 'docs_unexpected_host', 'docs_download'):
                continue
            raise
        file_id = drive + '!' + item_id
        title, link = item.get('name'), item.get('webUrl')
        for c in word_comments(data):
            at = stamp(c['date']) or stamp(item.get('lastModifiedDateTime'))
            mention = owner in c['mailto']
            if not at or not c['text'] or (not owned and not mention):
                continue
            key = short_id(file_id, 'comment', c['id'], c['date'], c['author'])
            if key in seen:
                continue
            seen[key] = 'comment'
            if since is None and at < start:
                continue
            events.append(event(account, 'docs.mention' if mention else 'docs.comment', key, at.isoformat(), title,
                                f"{c['author'] or 'Someone'}: {c['text']}",
                                {'provider': 'microsoft', 'file_id': file_id, 'comment_id': c['id'], 'doc_title': title,
                                 'from': c['author'], 'from_name': c['author'], 'to': owner, 'owned': owned, 'mention': mention,
                                 **({'source_url': link} if str(link or '').startswith('https://') else {})}))
        if owned:
            found = {ch['id'] + ':' + ch['date']: f"{ch['verb']}: {ch['text']}" for ch in word_changes(data)}
            known = set(marks.get(file_id) or [])
            new = [text for sid, text in found.items() if sid not in known]
            authors = {ch['author'] for ch in word_changes(data)}
            if found or file_id in marks:
                marks[file_id] = sorted(found)[:500]
            editor = person((item.get('lastModifiedBy') or {}).get('user'))
            if new and since is not None and editor[1] != owner:
                changed = stamp(item.get('lastModifiedDateTime')) or now
                events.append(suggestion_event(account, owner, 'microsoft', file_id, title, changed.isoformat(), new,
                                               editor if editor[0] or editor[1] else (', '.join(sorted(authors))[:120], ''), link))
    remaining = pending[MAX_FILES:]
    cycle_at = state.get('word_cycle_at') or now.isoformat()
    return events, {'seen': trim(seen), 'suggested': dict(list(marks.items())[-200:]),
                    'delta': state.get('delta') if remaining else token, 'word_pending': remaining,
                    'word_next': token if remaining else None, 'word_cycle_at': cycle_at if remaining else None,
                    'more': bool(remaining), 'caught_up_at': cycle_at}


def sync(store, config, account, helpers):
    state = dict(store.checkpoint(account['id']) or {})
    now = stamp(helpers.now())
    kind = provider(config, account)
    events, kept = (sync_microsoft if kind == 'microsoft' else sync_google)(store, config, account, helpers, state, now)
    more = kept.pop('more', False)
    caught_up_at = kept.pop('caught_up_at', now.isoformat())
    state.update(kept, provider=kind, coverage_complete=not more, replies=replies_on(config, account, helpers),
                 writes=sorted(writes_on(config, account, helpers)),
                 coverage=('Word and OneDrive' if kind == 'microsoft' else 'Google Docs') + (' catching up.' if more else ' caught up.'))
    if not more:
        state['since'] = caught_up_at
    store.commit_page(account['id'], state, events)
    return {'mode': 'incremental', 'events': len(events)}


def check(config, account, helpers):
    """A real read without storing anything: the docs sign-in is the owner's address and may read their files."""
    source = source_for(config, account, helpers)
    me = source.me()
    email = str(me.get('emailAddress') or '').lower()
    if email and email != str(account.get('email') or '').lower():
        raise helpers.SourceError('account_identity_mismatch')
    return None


def replies_on(config, account, helpers):
    """Google only, with the separate reply consent: posting a reply to a comment. Microsoft Graph cannot reply to a
    Word comment, and a Fleet-shared connection only reads."""
    if account.get('shared') or provider(config, account) != 'google':
        return False
    try:
        return REPLY_SCOPE in google_scopes(config, helpers, signin(config, account, helpers))
    except Exception:  # noqa: BLE001 - unknown means off: the draft stays a draft to post by hand
        return False


def read_text(config, account, file_id, helpers):
    """A doc's title, link and text (at most MAX_TEXT characters), read once for a run the owner started."""
    info, text = source_for(config, account, helpers).text(file_id)
    return {'title': info.get('name'), 'url': info.get('webViewLink') or info.get('webUrl'), 'text': text[:MAX_TEXT],
            'truncated': len(text) > MAX_TEXT}


def find(config, account, words, helpers):
    """Docs of this connection that match the words (at most MAX_FOUND), for a run the owner started: read-only."""
    words = ' '.join(str(words or '').split())[:200]
    if not words:
        raise helpers.SourceError('docs_find_empty')
    return source_for(config, account, helpers).find(words)


def doc_links(text):
    """The Google Doc ids linked in a text (docs.google.com/document/d/<id>), in order, once each."""
    return list(dict.fromkeys(DOC_LINK.findall(str(text or ''))))


def refresh(store, config, account, helpers):
    """An action-only connection (Brings in signals off): nothing read, only what it may do now (replies and writes),
    kept on its checkpoint for its card, without counting as a sync."""
    state = dict(store.checkpoint(account['id']) or {})
    state.update(provider=provider(config, account), replies=replies_on(config, account, helpers),
                 writes=sorted(writes_on(config, account, helpers)), coverage='Action-only: nothing synced.')
    store.commit_page(account['id'], state, [], record_sync=False)


class Replier(Google):
    """The one write: a reply to one comment, as the owner, only with the reply consent."""

    def __init__(self, config, account, helpers):
        if account.get('shared') or provider(config, account) != 'google':
            raise helpers.SourceError('docs_replies_unsupported')
        super().__init__(config, account, helpers)

    def comment(self, file_id, comment_id):
        return self.call('drive.comments.get', {'fileId': file_id, 'commentId': comment_id,
                                                'fields': 'id,deleted,replies(id,author(me),content,createdTime)'})

    def mine(self, comment):
        return [(str(r.get('id')), str(r.get('createdTime') or ''), ' '.join(str(r.get('content') or '').split()))
                for r in comment.get('replies') or [] if isinstance(r, dict) and (r.get('author') or {}).get('me')]

    def reply(self, file_id, comment_id, body):
        return self.call('drive.replies.create', {'fileId': file_id, 'commentId': comment_id, 'fields': 'id,content,createdTime'},
                         scope=REPLY_SCOPE, body={'content': body}, write=True)


def google_reason(text):
    """Google's label for a refusal in its error body (google_api.error_reason): SERVICE_DISABLED, storageQuotaExceeded..."""
    import google_api  # noqa: PLC0415
    return google_api.error_reason(text)


def gog_google(account):
    """The owner's own Google sign-in through gog (a Gmail account, not one a Fleet shares): a place for a new Google Doc
    with the scopes that sign-in already has (drive or drive.file). Nothing asks gog for more."""
    return (account.get('service', 'gmail') == 'gmail' and account.get('transport') == 'gog' and bool(account.get('email'))
            and not account.get('shared'))


class GogGoogle:
    """Google Docs and Drive calls with the owner's gog sign-in (`gog api call`), like the calendar and Gmail writes:
    reads with --readonly, a write only with --allow-write, and only the scope it is given."""
    VERSIONS = {'drive': 'v3', 'docs': 'v1'}

    def __init__(self, config, account, helpers):
        self.config, self.account, self.helpers = config, account, helpers
        self.signin = account

    def drive_scope(self):
        """The Drive scope this sign-in already has for docs: drive, else drive.file. Every call uses it (gog's sign-in
        may not hold drive.readonly), never a scope it doesn't have."""
        if not hasattr(self, '_scope'):
            import next_actions  # noqa: PLC0415
            try:
                granted = next_actions.granted_scopes(self.config, self.helpers.credential, self.account)
            except Exception:  # noqa: BLE001
                granted = set()
            self._scope = REPLY_SCOPE if REPLY_SCOPE in granted else FILE_SCOPE
        return self._scope

    def call(self, method, params, scope=READ_SCOPE, body=None, write=False, **_):
        scope = self.drive_scope() if scope in (READ_SCOPE, REPLY_SCOPE, FILE_SCOPE) else scope
        import os  # noqa: PLC0415
        import subprocess  # noqa: PLC0415
        import tempfile  # noqa: PLC0415
        api = method.split('.', 1)[0]
        env = {**os.environ, 'GOG_KEYRING_BACKEND': 'file', 'GOG_KEYRING_PASSWORD': self.helpers.credential(self.config, 'gog-password')}
        env.pop('DBUS_SESSION_BUS_ADDRESS', None)
        with tempfile.NamedTemporaryFile('w', suffix='.json') as file:
            file.write(json.dumps(body if body is not None else {}, ensure_ascii=False))
            file.flush()
            command = [self.config.get('gog') or 'gog', 'api', 'call', api, self.VERSIONS[api], method, '--params', json.dumps(params),
                       *(['--body', '@' + file.name] if body is not None else []), '--scope', scope, '--account', self.account['email'],
                       *(['--client', self.account['client']] if self.account.get('client') else []),
                       *(['--allow-write', '--force'] if write else ['--readonly']), '--no-input', '--json']
            try:
                result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=60)
            except subprocess.TimeoutExpired:
                raise self.helpers.SourceError('docs_timeout') from None
        if result.returncode:
            said = (result.stderr or '') + '\n' + (result.stdout or '').replace('\\"', '"')
            found = re.search(r'"code":\s*(\d{3})\b', said) or re.search(r'\b(4\d\d|5\d\d)\b', result.stderr or '')
            error = self.helpers.SourceError('docs_google', int(found[1]) if found else None)
            error.reason = google_reason(said)  # Google's own label for it (SERVICE_DISABLED, storageQuotaExceeded...), never text
            raise error
        try:
            return json.loads(result.stdout or '{}')
        except ValueError:
            raise self.helpers.SourceError('docs_google') from None


def writes_on(config, account, helpers):
    """What this Docs connection may write after the owner's OK: {'create', 'edit'}, a part, or nothing. Google: the
    drive scope (the same consent as posting replies) for both, drive.file for a new doc only. Microsoft:
    Files.ReadWrite.All, from Allow edits. A gog Google sign-in: a new doc only, when it has drive or drive.file
    already. A Fleet-shared connection only reads; unknown means nothing."""
    if account.get('shared'):
        return set()
    if gog_google(account):
        try:
            import next_actions  # noqa: PLC0415
            granted = next_actions.granted_scopes(config, helpers.credential, account)
        except Exception:  # noqa: BLE001 - unknown means off
            return set()
        return {'create'} if granted & {REPLY_SCOPE, FILE_SCOPE} else set()
    try:
        sign = signin(config, account, helpers)
        if provider(config, account) == 'microsoft':
            import ms_graph
            granted = {str(s).rsplit('/', 1)[-1] for s in ms_graph.scopes(config, helpers.credential, sign)}
            return {'create', 'edit'} if MS_WRITE_SCOPE in granted else set()
        granted = google_scopes(config, helpers, sign)
        # drive does both; documents edits a doc by its id, drive.file makes a new one (a Google Docs sign-in has these two)
        return ({'create'} if granted & {REPLY_SCOPE, FILE_SCOPE} else set()) | ({'edit'} if granted & {REPLY_SCOPE, DOCS_SCOPE} else set())
    except Exception:  # noqa: BLE001 - unknown means off: the change stays text in the to-do
        return set()


class Writer:
    """The doc writes (doc_writes.py decides what): a new doc, or an edit pinned to the version the owner approved."""

    def __init__(self, config, account, helpers):
        if account.get('shared'):
            raise helpers.SourceError('docs_writes_unsupported')
        self.provider, self.helpers, self.config, self.account = provider(config, account), helpers, config, account
        self.gog = gog_google(account)
        self.source = (GogGoogle if self.gog else Microsoft if self.provider == 'microsoft' else Google)(config, account, helpers)

    def scope(self):
        """Google: drive when granted (any doc), else drive.file (only docs this app created)."""
        if self.gog:
            return self.source.drive_scope()
        granted = self.granted()
        return REPLY_SCOPE if REPLY_SCOPE in granted or FILE_SCOPE not in granted else FILE_SCOPE

    def granted(self):
        """The Google sign-in's scopes (unknown: none)."""
        import google_api
        try:
            return google_scopes(self.config, self.helpers, self.source.signin)
        except google_api.BrokerError:
            return set()

    def docs_write_scope(self):
        """An edit through the Docs API: drive when granted, else documents (a Google Docs sign-in's)."""
        return DOCS_SCOPE if not self.gog and REPLY_SCOPE not in self.granted() and DOCS_SCOPE in self.granted() else REPLY_SCOPE

    def make(self, token, title, body, upload, fill):
        """A new Google Doc in the owner's My Drive, tagged with this write's token (appProperties) so an unclear outcome
        is found again (written), never made twice. Drive takes no pre-generated id for a Google Doc ("pre-generated IDs
        aren't supported for the creation of Google Workspace files": a 403 on 2026-11-03), so Drive picks the id. Through
        the broker one upload of its HTML; with gog (JSON bodies only) an empty doc, then its text in one batchUpdate
        pinned to that empty doc."""
        if not self.gog:
            return self.upload(*upload)
        made = self.source.call('drive.files.create', {'fields': 'id,name,webViewLink'}, scope=self.scope(), write=True,
                                body={'name': title, 'mimeType': DOC_MIME, 'appProperties': {WRITE_KEY: token}})
        if made.get('id'):
            self.fill(str(made['id']), fill)
        return made

    def fill(self, file_id, fill):
        """Writes the new doc's text into it while it is still empty (never twice: a doc with text is left as it is)."""
        doc = self.document(file_id)
        if ''.join(str((e.get('textRun') or {}).get('content') or '') for b in ((doc.get('body') or {}).get('content') or [])
                   for e in ((b.get('paragraph') or {}).get('elements') or [])).strip():
            return False
        self.update(file_id, fill, str(doc.get('revisionId') or ''))
        return True

    # Google Docs
    def document(self, file_id):
        # a Google Docs sign-in (documents, drive.file) reads any doc by its id with documents, not only the ones it made
        scope = DOCS_SCOPE if not self.gog and DOCS_SCOPE in self.granted() and READ_SCOPE not in self.granted() else None
        return self.source.call('docs.documents.get', {'documentId': file_id}, **({'scope': scope} if scope else {}))

    def update(self, file_id, requests, revision):
        return self.source.call('docs.documents.batchUpdate', {'documentId': file_id}, scope=self.docs_write_scope(), write=True,
                                body={'requests': requests, 'writeControl': {'requiredRevisionId': revision}})

    def written(self, token):
        """The doc this write made (its appProperties token), or None: how an unclear create is checked."""
        found = self.source.call('drive.files.list', {
            'q': f"appProperties has {{ key='{WRITE_KEY}' and value='{token}' }} and trashed = false",
            'fields': 'files(id,name)', 'pageSize': 2, 'spaces': 'drive'}, scope=self.scope())
        files = (found.get('files') or []) if isinstance(found, dict) else []
        return files[0] if files else None

    def upload(self, data, content_type):
        return self.source.call('drive.files.upload', {'uploadType': 'multipart', 'fields': 'id,name,webViewLink'},
                                scope=self.scope(), body=data, content_type=content_type, write=True)

    def find(self, file_id):
        try:
            return self.source.call('drive.files.get', {'fileId': file_id, 'fields': 'id,name,trashed', 'supportsAllDrives': True},
                                    scope=self.scope())
        except self.helpers.SourceError as error:
            if error.status == 404:
                return None
            raise

    # Word on OneDrive and SharePoint
    def item_and_bytes(self, file_id):
        drive, _, item_id = str(file_id).partition('!')
        item = self.source.item(drive, item_id)
        if not str(item.get('name') or '').lower().endswith('.docx'):
            raise self.helpers.SourceError('docs_edit_unsupported')
        return item, self.source.download(item)

    def put(self, file_id, data, etag):
        drive, _, item_id = str(file_id).partition('!')
        if not etag:
            raise self.helpers.SourceError('docs_microsoft', 412)
        return self.source.call('drives.item.content', {'drive': drive, 'id': item_id}, body=data, content_type=DOCX_MIME,
                                write=True, headers={'If-Match': etag})

    def lookup(self, name):
        try:
            return self.source.call('drive.root.item', {'name': name})
        except self.helpers.SourceError as error:
            if error.status == 404:
                return None
            raise

    def create(self, name, data):
        return self.source.call('drive.root.upload', {'name': name, '@microsoft.graph.conflictBehavior': 'fail'}, body=data,
                                content_type=DOCX_MIME, write=True)
