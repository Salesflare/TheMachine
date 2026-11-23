"""Notion as a connection: comments, mentions, tasks assigned to the owner and new pages, and, after the owner's OK,
a reply to a comment, a new private page, an edit to a page and marking a task done.

What comes in (each an event, linked to people like mail), from the pages the integration may see:
- notion.comment: someone else's comment on a page the owner made, or a reply in a discussion they are in.
- notion.mention: a comment that @mentions the owner.
- notion.task: a database item a person property assigns to the owner, with its due date and status. It shows in
  Calendar through its to-do's due date. Once Notion says it is done (a status in the Complete group, a checked
  checkbox, or a status named Done or Closed), the same event says so and its to-do closes (Store.close_done_notion).
- notion.page: a new page someone else added. Notion's API has no "shared with me": a page that newly shows up for
  the integration, made by someone else, is the closest it tells.
- notion.edit: someone else changed a page on which the owner has an open comment (they asked for a change): a quiet
  heads-up, never a buzz (machine/todo_kinds.py notion_edits).
The first sync goes back 7 days (bootstrap_days).

Two ways in:
- Sign in with Notion (the usual one): The Machine's public integration, through the hosting control plane, which
  exchanges the code with the integration's client secret and hands the result here sealed, as the credential, JSON:
  {access_token, refresh_token?, expires_at, bot_id, workspace_id, workspace_name, owner_id?, owner_email?}. Notion
  needs the client secret to refresh, which only the control plane has, so a refresh goes through it (POST
  /api/notion/token for a hosted Machine, <Network>/notion-token for a paired one): it uses the refresh token for that
  one call and keeps nothing. The new pair is kept here, in the same private credential file.
- A pasted internal integration token (the fallback), from https://www.notion.so/profile/integrations: the owner
  shares pages with it in Notion. The owner is found among the workspace's people by one of their own addresses.

The integration's capabilities, and only these: read content (pages, blocks, databases), update content (an approved
edit, marking a task done), insert content (a new page), read comments, insert comments (an approved reply), and user
information with email addresses (people are linked to the Graph by their address; without one, by an exact full name
that only one person in the Graph has).

Abilities (abilities.py): Brings in signals is the sync. Can do things: reading one page for a to-do or a meeting prep
(read_text, find), and the writes, each only after the owner's OK on exactly that (connectors/docs.py hands Docs'
transports to this module for a Notion connection): Replier for a doc_reply, Writer for a doc_write (doc_writes.py).
An edit writes only into the page as the owner saw it: its version is a digest of its blocks, read again right
before the write, and a page that changed since is left alone."""
import datetime as dt
import hashlib
import http.client
import json
import os
from pathlib import Path
import re
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

from machine import kinds as kind_rows

KINDS = {kind: row['name'] for kind, row in kind_rows.KINDS.items() if row['service'] == 'notion'}  # machine/kinds.py says
# How each kind reads in the message viewer (email, chat, notification or card) and the app its link opens in
# (machine/store/message_view.py; docs/adding-a-source.md, "How a message reads")
VIEWS = {kind: 'card' for kind in KINDS}
APP = 'Notion'
TOKEN_URL = 'https://www.notion.so/profile/integrations'
SETUP = {
    'label': 'Notion',
    'what': 'Comments, mentions and your tasks. Replies and edits you approve.',
    'account': {'id': 'notion', 'service': 'notion', 'transport': 'api', 'boundary': 'work', 'credential': 'notion',
                'poll_seconds': 600},
    # Sign in with Notion answers this same prompt with its sign-in (JSON); pasting an internal integration token is
    # the fallback. No workspace to type: the token says which one it is (GET /v1/users/me).
    'secret': 'Notion token',
    'token_url': TOKEN_URL,
    # Signed in at the hosting control plane (hosted: its account page; self-hosted: paired, from Connections, + Add)
    'account_page': 'source-notion',
    'note': 'Sign in with Notion from Connections, + Add. Or make an internal integration at '
            'https://www.notion.so/profile/integrations, share your pages with it and paste its token here.',
    'hints': {'notion_signin_expired': 'Notion asks you to sign in again',
              'notion_owner_unknown': 'Allow the integration to read user information with email addresses'},
    'errors': {'notion_signin_expired': ('Notion didn’t accept that sign-in', 'sign in with Notion again'),
               'notion_http:HTTP_401': ('Notion didn’t accept that token', 'copy it again from Notion and paste it here'),
               'notion_credential_unavailable': ('That doesn’t look like a Notion token', 'copy it again from Notion and paste it here'),
               'notion_owner_unknown': ('Notion didn’t say who you are in that workspace',
                                        'allow the integration to read user information with email addresses'),
               'notion_network': ('Notion didn’t answer', 'try again in a minute'),
               'account_identity_mismatch': ('That token is for another Notion workspace', 'add it as another Notion account')},
}
API = 'https://api.notion.com/v1/'
VERSION = '2022-06-28'
REFRESH_EARLY = 300  # seconds before the access token runs out that it is refreshed
TOKEN = re.compile(r'[A-Za-z0-9_.~+/=-]{8,2048}')
PASTED = re.compile(r'(?:secret_|ntn_)[A-Za-z0-9]{20,200}')
ID = re.compile(r'[0-9a-f]{32}')
LINK = re.compile(r'https://(?:www\.)?notion\.(?:so|site)/[^\s"\'<>)]*?([0-9a-f]{32})(?=[?#\s"\'<>)]|$)')
OVERLAP_HOURS = 2
MAX_PAGES = 40       # pages looked at per run, most recently edited first
MAX_SEARCH = 4       # search pages of 50 per run
MAX_BLOCKS = 25      # top-level blocks whose inline comments are read, on a page the owner made
MAX_TEXT = 200_000
MAX_FOUND = 10
SEEN_KEEP = 2000
PEOPLE_KEEP = 500
TEXT_BLOCKS = ('paragraph', 'heading_1', 'heading_2', 'heading_3', 'bulleted_list_item', 'numbered_list_item', 'to_do',
               'quote', 'callout', 'toggle')
NEW_BLOCK = {'h1': 'heading_1', 'h2': 'heading_2', 'h3': 'heading_3', 'p': 'paragraph'}
FIXED = '￼'  # a mention or an equation in a paragraph: never part of a change
DONE_WORDS = re.compile(r'(?i)\s*(?:done|complete|completed|closed|finished|resolved|cancell?ed|archived)\s*')
DUE_WORDS = re.compile(r'(?i)due|deadline|date|when')
# The calls this connector makes, as (method, path pattern). Writes only through Writer and Replier.
READS = (('GET', r'users/me'), ('GET', r'users/[0-9a-f-]{32,36}'), ('GET', r'users'), ('POST', r'search'),
         ('GET', r'comments'), ('GET', r'blocks/[0-9a-f-]{32,36}/children'), ('GET', r'pages/[0-9a-f-]{32,36}'),
         ('GET', r'databases/[0-9a-f-]{32,36}'))
WRITES = (('POST', r'comments'), ('PATCH', r'blocks/[0-9a-f-]{32,36}'), ('PATCH', r'blocks/[0-9a-f-]{32,36}/children'),
          ('PATCH', r'pages/[0-9a-f-]{32,36}'), ('POST', r'pages'))


def signin(secret):
    """The sign-in from Sign in with Notion, or None for a pasted token."""
    if not secret.startswith('{'):
        return None
    try:
        value = json.loads(secret)
    except ValueError:
        return None
    if not isinstance(value, dict) or not isinstance(value.get('access_token'), str) or not TOKEN.fullmatch(value['access_token']) \
            or not isinstance(value.get('refresh_token', ''), str) or (value.get('refresh_token') and not TOKEN.fullmatch(value['refresh_token'])) \
            or not isinstance(value.get('expires_at', 0), (int, float)) or not isinstance(value.get('bot_id', ''), str):
        return None
    return value


def plain_id(value):
    """A Notion id without its dashes, lowercased; '' for anything else."""
    text = str(value or '').replace('-', '').lower()
    return text if ID.fullmatch(text) else ''


def dashed(value):
    v = plain_id(value)
    return f'{v[:8]}-{v[8:12]}-{v[12:16]}-{v[16:20]}-{v[20:]}' if v else ''


def stamp(value):
    try:
        parsed = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    except (TypeError, ValueError):
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)


def short_id(*parts):
    return hashlib.sha256('\x00'.join(str(p) for p in parts).encode()).hexdigest()[:32]


def oneline(text, size=1000):
    return ' '.join(str(text or '').split())[:size]


def rich_plain(runs):
    """The text of a rich text array as the owner reads it (a mention by its name)."""
    return ''.join(str(r.get('plain_text') or (r.get('text') or {}).get('content') or '') for r in runs or () if isinstance(r, dict))


def mentioned(runs, user_id):
    """Whether a rich text array @mentions this person."""
    return bool(user_id) and any(isinstance(r, dict) and r.get('type') == 'mention' and (r.get('mention') or {}).get('type') == 'user'
                                 and plain_id(((r.get('mention') or {}).get('user') or {}).get('id')) == user_id for r in runs or ())


def page_title(page):
    """A page's title (its title property), or a database item's."""
    for prop in ((page or {}).get('properties') or {}).values():
        if isinstance(prop, dict) and prop.get('type') == 'title':
            return oneline(rich_plain(prop.get('title')), 200)
    return ''


def notion_links(text):
    """The Notion page ids linked in a text (notion.so/...<id>), in order, once each."""
    return list(dict.fromkeys(LINK.findall(str(text or ''))))


def refresh_place(config, helpers):
    """(url, credential name) where this Machine refreshes a Notion sign-in: its own control plane. Hosted: its broker's
    host, with its broker credential. Self-hosted and paired: the Network, with its own device token."""
    if config.get('manage_url'):
        base = (config.get('google_broker') or {}).get('url') or config['manage_url']
        parts = urllib.parse.urlsplit(str(base))
        if parts.scheme != 'https' or not parts.netloc:
            raise helpers.SourceError('notion_signin_expired')
        return f'https://{parts.netloc}/api/notion/token', 'google-broker'
    import fleet  # noqa: PLC0415
    home = fleet.settings(config)
    if not home or not str(home.get('url') or '').startswith('https://') or not (config.get('credentials') or {}).get('fleet'):
        raise helpers.SourceError('notion_signin_expired')
    return home['url'].rstrip('/') + '/notion-token', 'fleet'


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward the credential to a redirect target.


class Source:
    """Notion's API with the owner's sign-in or token: only READS, and WRITES for Writer and Replier."""

    def __init__(self, config, account, helpers):
        self.config, self.account, self.helpers = config, account, helpers
        self.name = account.get('credential', 'notion')
        try:
            secret = helpers.credential(config, self.name)
        except Exception:  # noqa: BLE001 - no file yet: the prompt asks for it
            raise helpers.SourceError('notion_credential_unavailable') from None
        secret = str(secret or '').strip()
        self.signin = signin(secret)
        if self.signin is None and not PASTED.fullmatch(secret):
            raise helpers.SourceError('notion_credential_unavailable')
        self.token = self.signin['access_token'] if self.signin else secret
        self.opener = urllib.request.build_opener(NoRedirect())
        self.people = {}
        if self.signin and self.signin.get('expires_at') and self.signin['expires_at'] - REFRESH_EARLY < time.time():
            self.refresh()

    def refresh(self):
        """A new access token from the control plane (it holds the integration's secret and keeps nothing), kept in the
        credential file. A sign-in that can't be refreshed any more: notion_signin_expired."""
        if not self.signin or not self.signin.get('refresh_token'):
            raise self.helpers.SourceError('notion_signin_expired')
        url, name = refresh_place(self.config, self.helpers)
        try:
            bearer = str(self.helpers.credential(self.config, name)).strip()
        except Exception:  # noqa: BLE001
            raise self.helpers.SourceError('notion_signin_expired') from None
        request = urllib.request.Request(url, method='POST', data=json.dumps(
            {'refresh_token': self.signin['refresh_token'], 'bot_id': self.signin.get('bot_id') or ''}).encode(),
            headers={'Authorization': 'Bearer ' + bearer, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        try:
            with self.opener.open(request, timeout=30) as response:
                answer = json.loads(response.read(200_001))
        except urllib.error.HTTPError as error:
            error.close()
            if error.code in (400, 401, 404, 409):
                raise self.helpers.SourceError('notion_signin_expired', error.code) from None
            raise self.helpers.SourceError('notion_http', error.code, retry_after=60 if error.code == 429 else None) from None
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException):
            raise self.helpers.SourceError('notion_network') from None
        except (ValueError, UnicodeError):
            raise self.helpers.SourceError('notion_invalid_json') from None
        access = answer.get('access_token') if isinstance(answer, dict) else None
        if not isinstance(access, str) or not TOKEN.fullmatch(access):
            raise self.helpers.SourceError('notion_signin_expired')
        rotated, expires = answer.get('refresh_token'), answer.get('expires_in')
        self.signin = {**self.signin, 'access_token': access,
                       **({'refresh_token': rotated} if isinstance(rotated, str) and TOKEN.fullmatch(rotated) else {}),
                       'expires_at': int(time.time() + expires) if isinstance(expires, int) and expires > 0 else 0}
        self.token = access
        self.keep()

    def keep(self):
        """The refreshed sign-in, written over the credential file (mode 600, replaced whole). One handed in by the
        service manager (CREDENTIALS_DIRECTORY) is read-only: then only this run uses the new token."""
        directory = os.environ.get('CREDENTIALS_DIRECTORY')
        if directory and (Path(directory) / self.name).exists():
            return
        place = (self.config.get('credentials') or {}).get(self.name)
        if not place:
            return
        path = Path(place).expanduser()
        fd, temp = tempfile.mkstemp(dir=path.parent, prefix='.' + path.name + '.')
        try:
            with os.fdopen(fd, 'w') as handle:
                handle.write(json.dumps(self.signin, separators=(',', ':')) + '\n')
            os.chmod(temp, 0o600)
            os.replace(temp, path)
        except OSError:
            if os.path.exists(temp):
                os.unlink(temp)
            raise self.helpers.SourceError('notion_credential_unwritable') from None

    def call(self, method, path, body=None, query=None, write=False, again=True):
        allowed = WRITES if write else READS
        if not any(method == m and re.fullmatch(p, path) for m, p in allowed):
            raise self.helpers.SourceError('notion_path_not_allowed')
        url = API + path + ('?' + urllib.parse.urlencode(query) if query else '')
        data = json.dumps(body, ensure_ascii=False).encode() if body is not None else None
        request = urllib.request.Request(url, method=method, data=data, headers={
            'Authorization': 'Bearer ' + self.token, 'Notion-Version': VERSION, 'Accept': 'application/json',
            'User-Agent': 'TheMachine/1', **({'Content-Type': 'application/json'} if data is not None else {})})
        route = re.sub(r'[0-9a-f-]{32,36}', '{id}', path)
        try:
            with self.opener.open(request, timeout=30) as response:
                raw = response.read(10_000_001)
            if len(raw) > 10_000_000:
                raise self.helpers.SourceError('notion_response_too_large', route=route)
            return json.loads(raw)
        except urllib.error.HTTPError as error:
            retry = error.headers.get('Retry-After', '') if error.headers else ''
            error.close()
            if error.code == 401 and self.signin and again:  # ran out early: one refresh, then it says so
                self.refresh()
                return self.call(method, path, body, query, write, again=False)
            if error.code == 401 and self.signin:
                raise self.helpers.SourceError('notion_signin_expired', 401, route=route) from None
            delay = min(3600, max(1, int(retry))) if retry.isdigit() else (60 if error.code == 429 else None)
            raise self.helpers.SourceError('notion_http', error.code, retry_after=delay, route=route) from None
        except (urllib.error.URLError, TimeoutError, OSError, http.client.HTTPException):
            raise self.helpers.SourceError('notion_network', route=route) from None
        except (ValueError, UnicodeError):
            raise self.helpers.SourceError('notion_invalid_json', route=route) from None

    # ------------------------------------------------------------------------------------------- who and where
    def verify(self):
        """GET /users/me: the integration's bot, its workspace and, for a sign-in, the person who signed in. A pasted
        token's owner is found among the workspace's people by one of the owner's own addresses. Keeps the workspace
        and the owner on the account (never the token)."""
        me = self.call('GET', 'users/me')
        bot = (me.get('bot') or {}) if isinstance(me, dict) else {}
        if not isinstance(me, dict) or me.get('type') != 'bot':
            raise self.helpers.SourceError('notion_invalid_me')
        self.bot_user = plain_id(me.get('id'))  # its own comments (an approved reply) are never news
        workspace = oneline(bot.get('workspace_name') or (self.signin or {}).get('workspace_name'), 100)
        space_id = plain_id((self.signin or {}).get('workspace_id')) or str(self.account.get('workspace_id') or '')
        if self.account.get('workspace_id') and space_id and self.account['workspace_id'] != space_id:
            raise self.helpers.SourceError('account_identity_mismatch')
        owner = (bot.get('owner') or {}) if isinstance(bot.get('owner'), dict) else {}
        user = owner.get('user') if owner.get('type') == 'user' and isinstance(owner.get('user'), dict) else {}
        member = plain_id(user.get('id') or (self.signin or {}).get('owner_id'))
        name = oneline(user.get('name'), 100)
        email = str(((user.get('person') or {}).get('email')) or (self.signin or {}).get('owner_email') or '').strip().lower()
        if not member:
            member, name, email = self.find_owner()
        if self.account.get('member_id') and member != self.account['member_id']:
            raise self.helpers.SourceError('account_identity_mismatch')
        self.account.update(member_id=member, workspace_name=workspace or 'Notion',
                            **({'workspace_id': space_id} if space_id else {}),
                            **({'member_name': name} if name else {}), **({'member_email': email} if '@' in email else {}))
        return {'id': member, 'name': name, 'email': email}

    def find_owner(self):
        """(id, name, email) of the owner among the workspace's people, by one of their own addresses."""
        mine = {str(a.get('email') or '').lower() for a in self.config.get('accounts', []) if '@' in str(a.get('email') or '')}
        mine |= {str(e).lower() for e in self.config.get('owner_emails') or () if '@' in str(e)}
        if self.account.get('member_email'):
            mine.add(self.account['member_email'])
        cursor = None
        for _ in range(10):
            try:
                page = self.call('GET', 'users', query={'page_size': 100, **({'start_cursor': cursor} if cursor else {})})
            except self.helpers.SourceError as error:
                if error.status == 403:
                    raise self.helpers.SourceError('notion_owner_unknown', 403) from None
                raise
            for u in page.get('results') or ():
                email = str(((u or {}).get('person') or {}).get('email') or '').lower()
                if u.get('type') == 'person' and email in mine:
                    return plain_id(u.get('id')), oneline(u.get('name'), 100), email
            cursor = page.get('next_cursor')
            if not page.get('has_more') or not cursor:
                break
        raise self.helpers.SourceError('notion_owner_unknown')

    def person(self, user_id, known):
        """(name, email) of a Notion person by id, asked once and kept in `known` (the checkpoint's people)."""
        uid = plain_id(user_id)
        if not uid:
            return '', ''
        if uid in known:
            return tuple(known[uid])
        try:
            u = self.call('GET', 'users/' + uid)
        except self.helpers.SourceError as error:
            if error.status in (403, 404):
                known[uid] = ['', '']
                return '', ''
            raise
        name = oneline(u.get('name'), 120) if isinstance(u, dict) else ''
        email = str(((u.get('person') or {}).get('email')) or '').strip().lower() if isinstance(u, dict) and u.get('type') == 'person' else ''
        known[uid] = [name, email if re.fullmatch(r'[^@\s<>]{1,64}@[^@\s<>]{1,253}', email) else '']
        return tuple(known[uid])

    # ------------------------------------------------------------------------------------------- reads
    def pages(self, since, cursor=None):
        """Pages edited since `since`, newest first, at most MAX_SEARCH searches: (pages, next cursor or None)."""
        found = []
        for _ in range(MAX_SEARCH):
            page = self.call('POST', 'search', body={'filter': {'property': 'object', 'value': 'page'},
                                                      'sort': {'direction': 'descending', 'timestamp': 'last_edited_time'},
                                                      'page_size': 50, **({'start_cursor': cursor} if cursor else {})})
            results = [p for p in page.get('results') or () if isinstance(p, dict) and plain_id(p.get('id'))]
            fresh = [p for p in results if (stamp(p.get('last_edited_time')) or since) >= since]
            found += fresh
            cursor = page.get('next_cursor')
            if len(fresh) < len(results) or not page.get('has_more') or not cursor:
                return found, None
        return found, cursor

    def comments(self, block_id):
        """The open comments on a page or block, oldest first (Notion lists only unresolved ones)."""
        out, cursor = [], None
        for _ in range(5):
            try:
                page = self.call('GET', 'comments', query={'block_id': dashed(block_id), 'page_size': 100,
                                                           **({'start_cursor': cursor} if cursor else {})})
            except self.helpers.SourceError as error:
                if error.status in (403, 404):
                    return out  # comments closed to this integration, or the page is gone
                raise
            out += [c for c in page.get('results') or () if isinstance(c, dict) and c.get('id')]
            cursor = page.get('next_cursor')
            if not page.get('has_more') or not cursor:
                break
        return out

    def children(self, block_id, limit=1000):
        out, cursor = [], None
        while len(out) < limit:
            page = self.call('GET', f'blocks/{plain_id(block_id)}/children',
                             query={'page_size': 100, **({'start_cursor': cursor} if cursor else {})})
            out += [b for b in page.get('results') or () if isinstance(b, dict) and b.get('id')]
            cursor = page.get('next_cursor')
            if not page.get('has_more') or not cursor:
                break
        return out[:limit]

    def page(self, page_id):
        return self.call('GET', 'pages/' + plain_id(page_id))

    def database(self, database_id, cache):
        key = plain_id(database_id)
        if key not in cache:
            try:
                cache[key] = self.call('GET', 'databases/' + key)
            except self.helpers.SourceError as error:
                if error.status not in (403, 404):
                    raise
                cache[key] = {}
        return cache[key]

    def text(self, page_id):
        """A page's title, link and text: its blocks, a line each, two levels deep."""
        page = self.page(page_id)
        lines = []

        def walk(block_id, depth):
            for b in self.children(block_id, 400):
                body = b.get(b.get('type')) if isinstance(b.get(b.get('type')), dict) else {}
                said = rich_plain(body.get('rich_text') or body.get('text'))
                if b.get('type') == 'child_page':
                    said = body.get('title') or ''
                elif b.get('type') in ('file', 'pdf'):  # a file on the page: its name (Notion's own link to it runs out in an hour)
                    said = '[file] ' + (oneline(body.get('name'), 200) or oneline(rich_plain(body.get('caption')), 200))
                if said.strip():
                    lines.append(('  ' * depth) + said)
                if b.get('has_children') and depth < 1 and b.get('type') not in ('child_page', 'child_database'):
                    walk(b['id'], depth + 1)
                if sum(len(x) for x in lines) > MAX_TEXT:
                    return
        walk(page_id, 0)
        return {'name': page_title(page), 'webViewLink': page.get('url')}, '\n'.join(lines)

    def find(self, words):
        page = self.call('POST', 'search', body={'query': words, 'filter': {'property': 'object', 'value': 'page'}, 'page_size': MAX_FOUND})
        return [{'file_id': plain_id(p['id']), 'title': page_title(p), 'url': p.get('url'), 'at': p.get('last_edited_time')}
                for p in page.get('results') or () if isinstance(p, dict) and plain_id(p.get('id'))][:MAX_FOUND]


# ------------------------------------------------------------------------------------------- tasks

def task_of(page, owner, schema):
    """{due, status, done} of a database item a person property assigns to the owner, else None."""
    if ((page.get('parent') or {}).get('type')) != 'database_id':
        return None
    props = page.get('properties') or {}
    if not any(isinstance(p, dict) and p.get('type') == 'people' and any(plain_id((u or {}).get('id')) == owner for u in p.get('people') or ())
               for p in props.values()):
        return None
    due, status, done = None, '', None
    dates = [(n, p) for n, p in props.items() if isinstance(p, dict) and p.get('type') == 'date' and (p.get('date') or {}).get('start')]
    if dates:
        name, prop = sorted(dates, key=lambda d: not DUE_WORDS.search(d[0]))[0]
        due = str((prop.get('date') or {}).get('end') or prop['date']['start'])[:25]
    groups = {}
    for n, p in ((schema or {}).get('properties') or {}).items():
        if isinstance(p, dict) and p.get('type') == 'status':
            for g in (p.get('status') or {}).get('groups') or ():
                for oid in g.get('option_ids') or ():
                    groups[oid] = str(g.get('name') or '')
    for n, p in props.items():
        if not isinstance(p, dict):
            continue
        if p.get('type') == 'status' and isinstance(p.get('status'), dict):
            status = oneline(p['status'].get('name'), 60)
            group = groups.get(p['status'].get('id'))
            done = (group.lower() == 'complete') if group else bool(DONE_WORDS.fullmatch(status))
        elif p.get('type') == 'checkbox' and done is None:
            done = bool(p.get('checkbox'))
            status = status or ('Checked' if done else 'Not checked')
        elif p.get('type') == 'select' and re.search(r'(?i)status|state|stage', n) and not status:
            status = oneline((p.get('select') or {}).get('name'), 60)
            done = bool(DONE_WORDS.fullmatch(status)) if status else False
    return {'due': due, 'status': status, 'done': bool(done)}


def done_change(page, schema):
    """(property name, the value that marks this item done) for a PATCH of its properties, or None."""
    props = page.get('properties') or {}
    for n, p in props.items():
        if isinstance(p, dict) and p.get('type') == 'status':
            spec = (((schema or {}).get('properties') or {}).get(n) or {}).get('status') or {}
            complete = next((g for g in spec.get('groups') or () if str(g.get('name') or '').lower() == 'complete'), None)
            options = {o.get('id'): o.get('name') for o in spec.get('options') or ()}
            chosen = next((options[i] for i in (complete or {}).get('option_ids') or () if options.get(i) and DONE_WORDS.fullmatch(options[i])),
                          next((options[i] for i in (complete or {}).get('option_ids') or () if options.get(i)), None))
            chosen = chosen or next((o for o in options.values() if o and DONE_WORDS.fullmatch(o)), None)
            if chosen:
                return n, {'status': {'name': chosen}}
    for n, p in props.items():
        if isinstance(p, dict) and p.get('type') == 'checkbox':
            return n, {'checkbox': True}
    for n, p in props.items():
        if isinstance(p, dict) and p.get('type') == 'select' and re.search(r'(?i)status|state|stage', n):
            options = [o.get('name') for o in (((schema or {}).get('properties') or {}).get(n) or {}).get('select', {}).get('options') or ()]
            chosen = next((o for o in options if o and DONE_WORDS.fullmatch(o)), None)
            if chosen:
                return n, {'select': {'name': chosen}}
    return None


# ------------------------------------------------------------------------------------------- events

def event(account, kind, key, at, title, body, meta, reviewed=False):
    return {'account_id': account['id'], 'source_id': kind.split('.')[1] + ':' + key, 'kind': kind, 'occurred_at': at,
            'title': oneline(title or 'Untitled', 1000), 'body': str(body or '')[:40000], 'metadata': meta, 'deleted': False,
            **({'reviewed': True} if reviewed else {})}


def sender(name, email):
    return f'{name} <{email}>' if name and email else email or name


def graph_email(store, name):
    """The address of the one Graph person with exactly this full name (two words or more), else ''. How someone whose
    Notion address the integration may not read is still linked, carefully: never a first name, never a name two people
    share."""
    name = oneline(name, 120)
    if len(name.split()) < 2 or not hasattr(store, 'connect'):
        return ''
    try:
        with store.connect() as db:
            rows = db.execute("SELECT info FROM graph_nodes WHERE kind='person' AND name=? COLLATE NOCASE LIMIT 3", (name,)).fetchall()
    except Exception:  # noqa: BLE001  (a Graph that is busy or not built yet: nobody linked, never a failed sync)
        return ''
    if len(rows) != 1:
        return ''
    try:
        ids = json.loads(rows[0][0] or '{}').get('ids') or []
    except (ValueError, TypeError):
        return ''
    emails = sorted({i[6:] for i in ids if isinstance(i, str) and i.startswith('email:')})
    return emails[0] if len(emails) == 1 else ''


def comment_events(account, store, source, owner, page, comments, start, seen, people, asked):
    """notion.comment and notion.mention events from one page's open comments, and the owner's open asks on it
    (`asked`: page id -> the time of their latest open comment, for the edit heads-up)."""
    out = []
    page_id = plain_id(page['id'])
    owned = plain_id((page.get('created_by') or {}).get('id')) == owner
    title = page_title(page) or 'Untitled'
    link = str(page.get('url') or '')
    threads = {}
    for c in comments:
        threads.setdefault(plain_id(c.get('discussion_id')) or plain_id(c.get('id')), []).append(c)
    for discussion, thread in threads.items():
        thread.sort(key=lambda c: str(c.get('created_time') or ''))
        mine = [c for c in thread if plain_id((c.get('created_by') or {}).get('id')) == owner]
        if mine:
            last = max(str(c.get('created_time') or '') for c in mine)
            asked[page_id] = max(asked.get(page_id, ''), last)
        for i, c in enumerate(thread):
            author = plain_id((c.get('created_by') or {}).get('id'))
            at = stamp(c.get('created_time'))
            if not author or author in (owner, getattr(source, 'bot_user', ''), plain_id((source.signin or {}).get('bot_id'))) or not at or at < start:
                continue
            key = short_id(page_id, discussion, plain_id(c.get('id')))
            edited = str(c.get('last_edited_time') or c.get('created_time'))
            if seen.get(key) == edited:
                continue
            mention = mentioned(c.get('rich_text'), owner)
            in_it = any(plain_id((p.get('created_by') or {}).get('id')) == owner for p in thread[:i])
            if not (mention or owned or in_it):
                continue
            seen[key] = edited
            name, email = source.person(author, people)
            matched = '' if email else graph_email(store, name)
            said = rich_plain(c.get('rich_text'))
            earlier = [f"{source.person(plain_id((p.get('created_by') or {}).get('id')), people)[0] or 'Someone'}: {rich_plain(p.get('rich_text'))}"
                       for p in thread[:i]][-5:]
            body = ('\n'.join(earlier) + '\n\n' if earlier else '') + f'{name or "Someone"}: {said}'
            url = link + ('&' if '?' in link else '?') + 'd=' + discussion if link.startswith('https://') else ''
            out.append(event(account, 'notion.mention' if mention else 'notion.comment', key, at.isoformat(), title, body, {
                'provider': 'notion', 'file_id': page_id, 'comment_id': discussion, 'reply_id': plain_id(c.get('id')),
                'doc_title': title, 'from': sender(name, email or matched), 'from_name': name,
                **({'from_email': email or matched} if email or matched else {}), **({'matched_by': 'name'} if matched else {}),
                'to': account.get('member_email') or '', 'owned': owned, 'mention': mention, **({'source_url': url} if url else {})}))
    return out


def trim(mapping, keep):
    return dict(list(mapping.items())[-keep:]) if len(mapping) > keep else mapping


def sync(store, config, account, helpers):
    source = Source(config, account, helpers)
    me = source.verify()
    owner = me['id']
    # the owner and this connection itself: a page it made or an edit it applied (each one approved) is never news
    us = {owner, getattr(source, 'bot_user', ''), plain_id((source.signin or {}).get('bot_id'))} - {''}
    state = dict(store.checkpoint(account['id']) or {})
    now = stamp(helpers.now())
    since = stamp(state.get('since'))
    cycle = dict(state.get('cycle') or {'at': now.isoformat()})
    start = (since - dt.timedelta(hours=OVERLAP_HOURS)) if since else stamp(cycle['at']) - dt.timedelta(days=int(config.get('bootstrap_days', 7)))
    seen, people = dict(state.get('seen') or {}), dict(state.get('people') or {})
    asked, tasks, edits = dict(state.get('asked') or {}), dict(state.get('tasks') or {}), dict(state.get('edits') or {})
    found, cursor = source.pages(start, cycle.get('cursor'))
    pending = list(cycle.get('pending') or []) + [p for p in found if plain_id(p['id']) not in {plain_id(q['id']) for q in cycle.get('pending') or []}]
    work, rest = pending[:MAX_PAGES], pending[MAX_PAGES:]
    schemas, events = {}, []
    for page in work:
        page_id = plain_id(page['id'])
        title = page_title(page) or 'Untitled'
        link = str(page.get('url') or '')
        meta = {'provider': 'notion', 'file_id': page_id, 'doc_title': title, **({'source_url': link} if link.startswith('https://') else {})}
        creator = plain_id((page.get('created_by') or {}).get('id'))
        created = stamp(page.get('created_time'))
        parent = (page.get('parent') or {}).get('type')
        # a task assigned to the owner: new, or its status, due date or title changed
        schema = source.database((page.get('parent') or {}).get('database_id'), schemas) if parent == 'database_id' else None
        task = task_of(page, owner, schema) if parent == 'database_id' else None
        if task:
            mark = [task['status'], task['due'], short_id(title), task['done']]
            before = tasks.get(page_id)
            if before != mark and not (before is None and task['done']):
                tasks[page_id] = mark
                when = f"Due {task['due'][:10]}." if task['due'] else 'No due date.'
                body = (f'Assigned to you in Notion. {when}' + (f" Status: {task['status']}." if task['status'] else '')
                        + (' Done in Notion.' if task['done'] else ''))
                events.append(event(account, 'notion.task', page_id, (stamp(page.get('last_edited_time')) or now).isoformat(), title, body,
                                    {**meta, 'task': True, 'due': task['due'], 'status': task['status'], 'done': task['done']},
                                    reviewed=bool(before is not None and (task['done'] or before[3]))))
            elif before is None:
                tasks[page_id] = mark
        elif page_id in tasks and parent == 'database_id':
            tasks.pop(page_id)  # no longer the owner's
        # a new page someone else added
        key = short_id(page_id, 'page')
        if parent != 'database_id' and created and created >= start and creator and creator not in us and key not in seen \
                and (page.get('created_by') or {}).get('object') == 'user' and since is not None:
            seen[key] = 'page'
            name, email = source.person(creator, people)
            if name or email:
                events.append(event(account, 'notion.page', page_id, created.isoformat(), title,
                                    f'{name or "Someone"} added “{title}” in Notion.',
                                    {**meta, 'from': sender(name, email), 'from_name': name, **({'from_email': email} if email else {}),
                                     'to': account.get('member_email') or ''}))
        elif key not in seen and created and creator and creator not in us:
            seen[key] = 'page'
        # comments: on the page, and inline on the first blocks of a page the owner made
        comments = source.comments(page_id)
        if creator == owner:
            for block in source.children(page_id, MAX_BLOCKS):
                comments += source.comments(block['id'])
        events += comment_events(account, store, source, owner, page, comments, start, seen, people, asked)
        # someone changed a page the owner asked to have changed (an open comment of theirs): a quiet heads-up
        editor = plain_id((page.get('last_edited_by') or {}).get('id'))
        edited = str(page.get('last_edited_time') or '')
        if page_id in asked and editor and editor not in us and edited > asked[page_id] and edits.get(page_id) != edited:
            edits[page_id] = edited
            name, email = source.person(editor, people)
            events.append(event(account, 'notion.edit', page_id + ':' + short_id(edited)[:12], (stamp(edited) or now).isoformat(), title,
                                f'{name or "Someone"} changed “{title}”, which you asked to have changed.',
                                {**meta, 'heads_up': True, 'from': sender(name, email), 'from_name': name,
                                 **({'from_email': email} if email else {}), 'to': account.get('member_email') or ''}))
    more = bool(rest or cursor)
    state.update(seen=trim(seen, SEEN_KEEP), people=trim(people, PEOPLE_KEEP), asked=trim(asked, 500), tasks=trim(tasks, 1000),
                 edits=trim(edits, 500), cycle={'at': cycle['at'], 'cursor': cursor, 'pending': rest} if more else None,
                 coverage_complete=not more, writes=sorted(writes_on(config, account, helpers)), replies=True,
                 coverage='Notion catching up.' if more else 'Notion caught up.')
    if not more:
        state['since'] = cycle['at']
    store.commit_page(account['id'], state, events)
    return {'mode': 'incremental', 'events': len(events), 'more': more}


def check(config, account, helpers):
    """A real read without storing anything: the token works and says who the owner is in which workspace."""
    Source(config, account, helpers).verify()


def refresh(store, config, account, helpers):
    """An action-only connection (Brings in signals off): nothing read, only what it may do, kept for its card."""
    state = dict(store.checkpoint(account['id']) or {})
    state.update(provider='notion', replies=not account.get('shared'), writes=sorted(writes_on(config, account, helpers)),
                 coverage='Action-only: nothing synced.')
    store.commit_page(account['id'], state, [], record_sync=False)


def read_text(config, account, file_id, helpers):
    """A page's title, link and text (at most MAX_TEXT characters), read once for a run the owner started."""
    info, text = Source(config, account, helpers).text(file_id)
    return {'title': info.get('name'), 'url': info.get('webViewLink'), 'text': text[:MAX_TEXT], 'truncated': len(text) > MAX_TEXT}


def find(config, account, words, helpers):
    words = oneline(words, 200)
    if not words:
        raise helpers.SourceError('docs_find_empty')
    return Source(config, account, helpers).find(words)


def writes_on(config, account, helpers):
    """What a Notion connection may write after the owner's OK: a new page, an edit, marking a task done. Its
    capabilities say whether Notion lets it; a refusal says so on the to-do. A Fleet-shared one only reads."""
    return set() if account.get('shared') else {'create', 'edit', 'done'}


def replies_on(config, account, helpers):
    return not account.get('shared')


# ------------------------------------------------------------------------------------------- the writes

class Replier(Source):
    """The one comment write: a reply in one discussion, after the owner's Post on exactly that text."""

    def __init__(self, config, account, helpers):
        if account.get('shared'):
            raise helpers.SourceError('docs_replies_unsupported')
        super().__init__(config, account, helpers)

    def thread(self, file_id, discussion):
        for c in self.comments(file_id):
            if plain_id(c.get('discussion_id')) == plain_id(discussion):
                return c
        for block in self.children(file_id, MAX_BLOCKS):
            for c in self.comments(block['id']):
                if plain_id(c.get('discussion_id')) == plain_id(discussion):
                    return c
        return None

    def comment(self, file_id, comment_id):
        """The discussion, as Docs' transport reads it: its replies, or {'deleted': True} once it is resolved or gone."""
        found = self.thread(file_id, comment_id)
        if not found:
            return {'deleted': True}
        replies = [c for c in self.comments(file_id) if plain_id(c.get('discussion_id')) == plain_id(comment_id)] or [found]
        return {'id': comment_id, 'replies': replies}

    def mine(self, comment):
        """[(id, created, text)] of the replies posted through this connection: as its integration, or as the owner."""
        bot = plain_id((self.signin or {}).get('bot_id'))
        if not bot:
            me = self.call('GET', 'users/me')
            bot = plain_id(me.get('id')) if isinstance(me, dict) else ''
        ours = {bot, plain_id(self.account.get('member_id'))} - {''}
        return [(plain_id(r.get('id')), str(r.get('created_time') or ''), ' '.join(rich_plain(r.get('rich_text')).split()))
                for r in comment.get('replies') or () if isinstance(r, dict) and plain_id((r.get('created_by') or {}).get('id')) in ours]

    def reply(self, file_id, comment_id, body):
        posted = self.call('POST', 'comments', write=True, body={'discussion_id': dashed(comment_id), 'rich_text': runs(body)})
        return {'id': plain_id(posted.get('id'))} if isinstance(posted, dict) else {}


def runs(text):
    """Plain text as Notion rich text (2000 characters a run at most)."""
    text = str(text)
    return [{'type': 'text', 'text': {'content': text[i:i + 2000]}} for i in range(0, len(text), 2000)] or [{'type': 'text', 'text': {'content': ''}}]


def new_blocks(body):
    import doc_writes  # noqa: PLC0415 - top-level module: the same lines() a Google Doc or Word file gets
    return [{'object': 'block', 'type': NEW_BLOCK[style], NEW_BLOCK[style]: {'rich_text': runs(text)}} for style, text in doc_writes.lines(body)]


def paragraphs(blocks):
    """The page's top-level text blocks as Docs' paragraphs: [{text, editable, id, runs}]. A mention or an equation is a
    FIXED character; other blocks (images, tables, code, child pages) are left out."""
    out = []
    for b in blocks:
        kind = b.get('type')
        if kind not in TEXT_BLOCKS or not isinstance(b.get(kind), dict):
            continue
        text = ''
        for r in b[kind].get('rich_text') or ():
            text += str((r.get('text') or {}).get('content') or '') if r.get('type') == 'text' else FIXED
        out.append({'text': text, 'editable': not b.get('archived'), 'id': plain_id(b['id']), 'kind': kind,
                    'runs': b[kind].get('rich_text') or []})
    return out


def version_of(page, blocks):
    """A page's version for an edit: a digest of its title and every top-level block as it is now. Notion stamps edits to
    the minute only, so the blocks themselves are compared."""
    parts = [page_title(page)] + [json.dumps([b.get('id'), b.get('type'), b.get('last_edited_time'), b.get(b.get('type'))],
                                             sort_keys=True, ensure_ascii=False) for b in blocks]
    return 'n:' + hashlib.sha256('\x00'.join(parts).encode()).hexdigest()[:40]


def replaced_runs(rich, start, end, new):
    """The block's rich text with [start, end) of its text replaced by `new`, every run around it as it was (its
    formatting and links); the new text takes the formatting of the first run it touches."""
    out, at, placed = [], 0, False
    for r in rich:
        size = len(str((r.get('text') or {}).get('content') or '')) if r.get('type') == 'text' else 1
        a, b = at, at + size
        at = b
        if b <= start or a >= end or r.get('type') != 'text':
            if a >= end and not placed and new:
                out.append({'type': 'text', 'text': {'content': new}})
                placed = True
            out.append(r)
            continue
        content = str(r['text'].get('content') or '')
        keep = {k: v for k, v in r.items() if k in ('type', 'annotations')}
        text = {k: v for k, v in r['text'].items() if k == 'link'}
        head, tail = content[:max(0, start - a)], content[max(0, end - a):]
        if head:
            out.append({**keep, 'text': {**text, 'content': head}})
        if not placed and new:
            out += [{**keep, 'text': {**text, 'content': new[i:i + 2000]}} for i in range(0, len(new), 2000)]
            placed = True
        if tail:
            out.append({**keep, 'text': {**text, 'content': tail}})
    if not placed and new:
        out.append({'type': 'text', 'text': {'content': new}})
    return out or [{'type': 'text', 'text': {'content': ''}}]


class Writer(Source):
    """The page writes (doc_writes.py decides what): a new private page, an edit pinned to the version the owner
    approved, a task marked done."""
    provider = 'notion'

    def __init__(self, config, account, helpers):
        if account.get('shared'):
            raise helpers.SourceError('docs_writes_unsupported')
        super().__init__(config, account, helpers)

    def snapshot(self, file_id):
        page = self.page(file_id)
        if page.get('archived') or page.get('in_trash'):
            raise self.helpers.SourceError('notion_http', 404)
        blocks = self.children(file_id)
        return {'version': version_of(page, blocks), 'title': page_title(page), 'url': str(page.get('url') or ''),
                'paragraphs': paragraphs(blocks)}

    def edit(self, file_id, changes, version):
        """The approved changes, only into the page as it was approved: read again right before, nothing written when it
        changed since (409)."""
        current = self.snapshot(file_id)
        if current['version'] != version:
            return {'rejected': 409}
        paras = current['paragraphs']

        def place(needle):
            found = [k for k, p in enumerate(paras) if needle in p['text']]
            if len(found) != 1 or paras[found[0]]['text'].count(needle) != 1:
                raise ValueError(needle)
            return found[0], paras[found[0]]['text'].index(needle)
        edits, inserts = {}, []
        try:
            for order, change in enumerate(changes):
                if 'find' in change:
                    k, s = place(change['find'])
                    if FIXED in change['find']:
                        return {'rejected': 409}
                    edits.setdefault(k, []).append((s, s + len(change['find']), change['replace']))
                elif 'after' in change:
                    k, _ = place(change['after'])
                    inserts.append((paras[k]['id'], order, change['insert']))
                else:
                    inserts.append((None, order, change['append']))
        except ValueError:
            return {'rejected': 409}
        for k, spans in edits.items():
            rich = paras[k]['runs']
            for s, e, new in sorted(spans, reverse=True):
                rich = replaced_runs(rich, s, e, new)
            self.call('PATCH', 'blocks/' + paras[k]['id'], write=True, body={paras[k]['kind']: {'rich_text': rich}})
        # after a paragraph: the later change first, so each lands right after its anchor in the owner's order; at the end:
        # in order
        anchored = sorted((x for x in inserts if x[0]), key=lambda x: -x[1])
        for after, _, text in anchored + [x for x in inserts if not x[0]]:
            blocks = new_blocks(text)
            for i in range(0, len(blocks), 100):
                made = self.call('PATCH', f'blocks/{plain_id(file_id)}/children', write=True,
                                 body={'children': blocks[i:i + 100], **({'after': dashed(after)} if after else {})})
                if after:  # the rest of a long insert follows the last block this one made
                    after = plain_id(((made or {}).get('results') or [{}])[-1].get('id')) or None
        return {'message_id': 'docwrite:' + plain_id(file_id)}

    def create(self, title, body, parent=None):
        """A new private page: in the owner's Private section, or under the page they chose (parent)."""
        blocks = new_blocks(body)
        where = {'type': 'page_id', 'page_id': dashed(parent)} if plain_id(parent) else {'type': 'workspace', 'workspace': True}
        made = self.call('POST', 'pages', write=True, body={'parent': where, 'properties': {'title': {'title': runs(title)}},
                                                              'children': blocks[:100]})
        page_id = plain_id((made or {}).get('id'))
        for i in range(100, len(blocks), 100):
            self.call('PATCH', f'blocks/{page_id}/children', write=True, body={'children': blocks[i:i + 100]})
        return {'id': page_id, 'url': (made or {}).get('url')}

    def written(self, title, since):
        """The page this write made, found again by its title, made by this integration since the write started."""
        page = self.call('POST', 'search', body={'query': title, 'filter': {'property': 'object', 'value': 'page'}, 'page_size': 20})
        bot = plain_id((self.signin or {}).get('bot_id'))
        for p in page.get('results') or ():
            if page_title(p) == oneline(title, 200) and (stamp(p.get('created_time')) or since) >= since \
                    and (not bot or plain_id((p.get('created_by') or {}).get('id')) == bot):
                return {'id': plain_id(p['id']), 'url': p.get('url')}
        return None

    def task(self, file_id):
        """(page, schema, change) of an assigned task: what marks it done, or None when it is done already."""
        page = self.page(file_id)
        schema = self.database((page.get('parent') or {}).get('database_id'), {}) if (page.get('parent') or {}).get('type') == 'database_id' else {}
        state = task_of(page, plain_id(self.account.get('member_id')), schema) or {}
        return page, schema, (None if state.get('done') else done_change(page, schema))

    def mark_done(self, file_id):
        page, _, change = self.task(file_id)
        if change is None:
            return {'message_id': 'docwrite:' + plain_id(file_id)}  # done in Notion already
        name, value = change
        self.call('PATCH', 'pages/' + plain_id(file_id), write=True, body={'properties': {name: value}})
        return {'message_id': 'docwrite:' + plain_id(file_id)}

