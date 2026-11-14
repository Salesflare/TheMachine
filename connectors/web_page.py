"""Watch a page (docs/help/web-page.md): one web page per connection, read on a schedule, a signal only when what it
says changed.

Config: {"id": "page", "service": "web_page", "transport": "http", "boundary": "work:Acme",
         "url": "https://example.com/pricing", "display_name": "example.com/pricing", "poll_seconds": 21600}

Each read is one plain HTTPS GET, as a polite reader: the site's robots.txt is asked first (kept a day), never more
than once an hour (MIN_SECONDS, also when Check now or a restart asks sooner), at most MAX_BYTES and TIMEOUT seconds,
and only to public addresses (every hop of a redirect, checked on the socket itself, so no name can point it at this
computer or its network). The page's main text (its <main> when it has one; no scripts, menus, footers, cookie or ad
boxes) is normalized into lines and hashed, with dates and times masked: a page whose only change is "Updated 2 hours
ago" never changes.

The first read keeps a baseline: one web_page.change event per page (source_id: the address's hash) that carries the
page's text in `page_text` (sealed like any message text, never shown to a review: REVIEW_METADATA_SKIP), marked as
already reviewed (`reviewed`, Store.commit_page), so it is never reviewed. Unchanged reads add nothing, so they cost no model call. A changed page is the same
event again, a new version: its body is what changed (− the lines it had, + the lines it has, a line around them),
and the signal review judges whether it matters (source-notes/web_page.md); a trivial change gets no to-do."""
import difflib
import gzip
import hashlib
import http.client
import ipaddress
import re
import socket
import time
import urllib.parse
import urllib.robotparser
import zlib
from html.parser import HTMLParser

KINDS = {'web_page.change': 'web page'}
# How it reads in the message viewer and the app its link opens in (machine/store/message_view.py)
VIEWS = {'web_page.change': 'card'}
APP = ''
SETUP = {'label': 'Web page', 'what': 'Changes that matter on a page you watch.',
         'account': {'id': 'page', 'service': 'web_page', 'transport': 'http', 'boundary': 'work', 'poll_seconds': 21600},
         'ask': [('url', 'Page address')],
         'hints': {'web_page_robots': 'this site asks automated readers to stay away from that page',
                   'web_page_address': 'use a public https:// address',
                   'web_page_not_html': 'that address is not a web page',
                   'web_page_empty': 'that page has no text without JavaScript',
                   'web_page_too_large': 'that page is too large to watch',
                   'web_page_http': 'the site answered with an error; check the address'}}

UA = 'TheMachine/1 (+page watch)'
ROBOTS_AGENT = 'TheMachine'
MIN_SECONDS = 3600  # never read a page more often than this
ROBOTS_SECONDS = 86400  # how long a robots.txt answer is kept
TIMEOUT = 10  # seconds per request, connect and read
MAX_BYTES = 2_000_000  # of a page; robots.txt gets ROBOTS_BYTES
ROBOTS_BYTES = 500_000
REDIRECTS = 5
TEXT_MAX = 40000  # characters of a page's text that are kept and compared
DIFF_MAX = 6000  # characters of what changed that a signal carries
CONTEXT = 1  # unchanged lines shown around a change
SKIP = {'script', 'style', 'noscript', 'template', 'svg', 'iframe', 'canvas', 'nav', 'footer', 'aside', 'form', 'select',
        'button', 'dialog', 'object', 'video', 'audio', 'map'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
BLOCK = {'p', 'div', 'section', 'article', 'main', 'header', 'li', 'ul', 'ol', 'dl', 'dt', 'dd', 'tr', 'table', 'h1',
         'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'hr', 'blockquote', 'pre', 'figure', 'figcaption', 'details', 'summary'}
NOISE = re.compile(r'(?i)(?:^|[\s_-])(?:cookies?|consent|gdpr|advert\w*|ads?|sponsored|popup)(?:$|[\s_-])')
# Dates, times and "3 hours ago": masked before comparing, so a page whose only change is when it was updated is unchanged
MONTH = r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?'
VOLATILE = re.compile(r'(?i)\b\d{4}-\d{2}-\d{2}(?:[t ]\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?(?:z|[+-]\d{2}:?\d{2})?)?\b'
                      r'|\b\d{1,2}[/.]\d{1,2}[/.]\d{2,4}\b'
                      r'|\b' + MONTH + r'\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s+\d{4})?\b'
                      r'|\b\d{1,2}(?:st|nd|rd|th)?\s+' + MONTH + r'(?:,?\s+\d{4})?\b'
                      r'|\b\d{1,2}:\d{2}(?::\d{2})?\s*(?:[ap]\.?m\.?)?'
                      r'|\b(?:\d+|an?|one)\s+(?:second|minute|min|hour|hr|day|week|month|year)s?\s+ago\b'
                      r'|\b(?:just now|yesterday|today)\b')


def address(value):
    """The page's address as kept: https, no fragment; a bare 'example.com/pricing' gets https://. ValueError when it
    isn't a web address."""
    value = ' '.join(str(value or '').split())
    if value and '://' not in value:
        value = 'https://' + value
    parts = urllib.parse.urlsplit(value)
    if parts.scheme == 'http':
        parts = parts._replace(scheme='https')
    if parts.scheme != 'https' or not parts.hostname or parts.username or parts.password or ' ' in value or len(value) > 2000:
        raise ValueError('not an https address')
    try:
        port = parts.port
    except ValueError:
        raise ValueError('not an https address') from None
    if port not in (None, 443):
        raise ValueError('not an https address')
    try:  # an address written as an IP: only a public one
        ip = ipaddress.ip_address(parts.hostname)
    except ValueError:
        ip = None
    if (ip is not None and not public(ip)) or parts.hostname == 'localhost' \
            or parts.hostname.endswith(('.localhost', '.local', '.internal', '.lan', '.home.arpa')):
        raise ValueError('not a public address')
    return urllib.parse.urlunsplit(parts._replace(fragment='', netloc=parts.netloc.lower()))


def page_name(url):
    """What its connection is called: the host and path, no www and no trailing slash ('example.com/pricing')."""
    parts = urllib.parse.urlsplit(url)
    host = re.sub(r'^www\.', '', parts.hostname or '')
    return (host + parts.path.rstrip('/'))[:120] or host


def public(ip):
    if getattr(ip, 'ipv4_mapped', None):
        ip = ip.ipv4_mapped
    return ip.is_global and not ip.is_multicast


def _connection(host, timeout, SourceError):
    def create(address_, *args, **kwargs):
        sock = socket.create_connection(address_, *args, **kwargs)
        try:
            peer = ipaddress.ip_address(sock.getpeername()[0])
        except (OSError, ValueError):
            sock.close()
            raise SourceError('web_page_address') from None
        if not public(peer):  # checked on the socket, after the name resolved: no rebinding around it
            sock.close()
            raise SourceError('web_page_address')
        return sock
    connection = http.client.HTTPSConnection(host, timeout=timeout)
    connection._create_connection = create
    return connection


def get(url, SourceError, headers=None, limit=MAX_BYTES):
    """One GET, following up to REDIRECTS redirects to public https addresses: (status, headers, body, final url).
    A 304 comes back with an empty body."""
    for _ in range(REDIRECTS + 1):
        try:
            url = address(url)
        except ValueError:
            raise SourceError('web_page_address') from None
        parts = urllib.parse.urlsplit(url)
        connection = _connection(parts.netloc, TIMEOUT, SourceError)
        try:
            connection.request('GET', (parts.path or '/') + (f'?{parts.query}' if parts.query else ''),
                               headers={'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,text/plain;q=0.9',
                                        'Accept-Encoding': 'gzip', **(headers or {})})
            response = connection.getresponse()
            if response.status in (301, 302, 303, 307, 308) and response.getheader('Location'):
                url = urllib.parse.urljoin(url, response.getheader('Location'))
                continue
            body = response.read(limit + 1) if response.status == 200 else b''
            return response.status, response.headers, body, url
        except (OSError, http.client.HTTPException):
            raise SourceError('web_page_network') from None
        finally:
            connection.close()
    raise SourceError('web_page_redirects')


def decoded(body, headers, limit, SourceError):
    if len(body) > limit:
        raise SourceError('web_page_too_large')
    if (headers.get('Content-Encoding') or '').lower() == 'gzip':
        try:
            inflate = zlib.decompressobj(16 + zlib.MAX_WBITS)
            body = inflate.decompress(body, limit + 1)
        except zlib.error:
            raise SourceError('web_page_not_html') from None
        if len(body) > limit or inflate.unconsumed_tail:
            raise SourceError('web_page_too_large')
    charset = re.search(r'charset=["\']?([\w.-]+)', headers.get('Content-Type') or '', re.I) \
        or re.search(rb'<meta[^>]+charset=["\']?([\w.-]+)', body[:4096], re.I)
    name = charset.group(1) if charset else 'utf-8'
    name = name.decode('ascii', 'replace') if isinstance(name, bytes) else name
    try:
        return body.decode(name, 'replace')
    except LookupError:
        return body.decode('utf-8', 'replace')


def robots_allow(url, SourceError):
    """Whether the site's robots.txt lets ROBOTS_AGENT read this page. No robots.txt (404, 410): yes; one that is
    refused (401, 403): no, as urllib.robotparser reads it. A site that can't answer: try again later."""
    parts = urllib.parse.urlsplit(url)
    status, headers, body, _ = get(f'https://{parts.netloc}/robots.txt', SourceError, limit=ROBOTS_BYTES)
    if status in (401, 403):
        return False
    if status != 200:
        if status >= 500 or status == 429:
            raise SourceError('web_page_http', status, retry_after=MIN_SECONDS)
        return True
    rules = urllib.robotparser.RobotFileParser()
    rules.parse(decoded(body, headers, ROBOTS_BYTES, SourceError).splitlines())
    return rules.can_fetch(ROBOTS_AGENT, url)


class _Text(HTMLParser):
    """A page's readable text, in lines: its <main> when it has one, without scripts, menus, footers, forms and boxes
    marked as a cookie notice or an ad."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.skipping, self.in_main, self.in_title, self.in_head = [], 0, 0, False, False
        self.all, self.main, self.title = [''], [''], ''

    def handle_starttag(self, tag, attrs):
        if tag in ('head', 'body', 'html'):  # never kept on the stack: a page that leaves </head> out still has a body
            self.in_head = tag == 'head'
            return
        if tag in VOID:
            if tag in BLOCK:
                self.newline()
            return
        a = dict(attrs)
        skip = tag in SKIP or 'hidden' in a or a.get('aria-hidden') == 'true' or a.get('role') in ('navigation', 'banner', 'contentinfo', 'dialog') \
            or bool(NOISE.search(' '.join(str(a.get(k) or '') for k in ('id', 'class'))))
        main = tag == 'main' or a.get('role') == 'main'
        self.stack.append((tag, skip, main))
        self.skipping += skip
        self.in_main += main
        self.in_title = tag == 'title' and self.in_head  # the page's own, never an icon's <title> in an <svg>
        if tag in BLOCK:
            self.newline()
        elif tag in ('td', 'th'):
            self.text(' ')

    def handle_startendtag(self, tag, attrs):
        if tag in BLOCK:
            self.newline()

    def handle_endtag(self, tag):
        if tag == 'head':
            self.in_head = False
        if not any(t == tag for t, _, _ in self.stack):
            return
        while self.stack:
            t, skip, main = self.stack.pop()
            self.skipping -= skip
            self.in_main -= main
            if t == tag:
                break
        self.in_title = False
        if tag in BLOCK:
            self.newline()

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif not self.skipping and not self.in_head:
            self.text(data)

    def text(self, data):
        self.all[-1] += data
        if self.in_main:
            self.main[-1] += data

    def newline(self):
        for lines in (self.all, self.main):
            if lines[-1].strip():
                lines.append('')


def page_text(html):
    """(title, lines) of a page: its main text as normalized lines (spaces collapsed, no empty or repeated lines),
    at most TEXT_MAX characters."""
    reader = _Text()
    try:
        reader.feed(html)
        reader.close()
    except (AssertionError, ValueError):  # an unreadable tag: what was read so far
        pass
    main = [' '.join(line.split()) for line in reader.main]
    lines = [line for line in main if line] if sum(map(len, main)) >= 200 else [' '.join(line.split()) for line in reader.all]
    out, size = [], 0
    for line in lines:
        if not line or (out and out[-1] == line):
            continue
        size += len(line) + 1
        if size > TEXT_MAX:
            break
        out.append(line)
    return ' '.join(reader.title.split())[:200], out


def masked(line):
    return VOLATILE.sub('#', line)


def fingerprint(lines):
    return hashlib.sha256('\n'.join(masked(line) for line in lines).encode()).hexdigest()


def changes(before, after):
    """What changed between two versions of a page's lines, as a signal's body: each change with a line around it, the
    lines it had as '− line', the lines it has as '+ line', changes apart by an empty line. '' when the only
    differences are dates and times."""
    a, b = [masked(line) for line in before], [masked(line) for line in after]
    hunks = []
    for group in difflib.SequenceMatcher(None, a, b, autojunk=False).get_grouped_opcodes(CONTEXT):
        lines = []
        for op, i1, i2, j1, j2 in group:
            if op == 'equal':
                lines += after[j1:j2]
            else:
                lines += ['− ' + line for line in before[i1:i2]] + ['+ ' + line for line in after[j1:j2]]
        hunks.append('\n'.join(lines))
    body, kept = '', 0
    for hunk in hunks:
        if len(body) + len(hunk) > DIFF_MAX:
            break
        body, kept = body + ('\n\n' if body else '') + hunk, kept + 1
    if hunks and not kept:
        body = hunks[0][:DIFF_MAX]
    return body


def read(url, state, SourceError):
    """(status, title, lines) of the page now, robots.txt asked first (kept ROBOTS_SECONDS in state): status 304 when
    it says it didn't change since the last read (ETag or Last-Modified)."""
    now = time.time()
    robots = state.get('robots') or {}
    if robots.get('url') != url or now - float(robots.get('at') or 0) > ROBOTS_SECONDS:
        robots = {'url': url, 'at': now, 'allow': robots_allow(url, SourceError)}
        state['robots'] = robots
    if not robots['allow']:
        raise SourceError('web_page_robots')
    headers = {}
    if state.get('etag'):
        headers['If-None-Match'] = state['etag']
    if state.get('last_modified'):
        headers['If-Modified-Since'] = state['last_modified']
    status, response, body, _ = get(url, SourceError, headers)
    if status == 304:
        return 304, '', None
    if status != 200:
        retry = response.get('Retry-After') if response else None
        raise SourceError('web_page_http', status, retry_after=max(MIN_SECONDS, int(retry)) if status in (429, 503) and str(retry or '').isdigit()
                          else MIN_SECONDS if status in (429, 503) else None)
    kind = (response.get('Content-Type') or 'text/html').split(';')[0].strip().lower()
    if kind not in ('text/html', 'application/xhtml+xml', 'text/plain'):
        raise SourceError('web_page_not_html')
    text = decoded(body, response, MAX_BYTES, SourceError)
    title, lines = page_text(text) if kind != 'text/plain' else ('', [' '.join(l.split()) for l in text.splitlines() if l.strip()])
    if not lines:
        raise SourceError('web_page_empty')
    state['etag'], state['last_modified'] = response.get('ETag'), response.get('Last-Modified')
    return 200, title, lines


def event(account, url, title, body, lines, stamp):
    return {'account_id': account['id'], 'source_id': hashlib.sha256(url.encode()).hexdigest(), 'kind': 'web_page.change',
            'occurred_at': stamp, 'title': (title or page_name(url))[:1000], 'body': body[:40000],
            'metadata': {'source_url': url, 'page_text': '\n'.join(lines)}, 'deleted': False}


def baseline(store, account):
    """The page's text as last kept (its event's page_text), or None before the first read."""
    rows = store.events([account['id']], limit=1, kinds=['web_page.change'])
    text = rows[0]['metadata'].get('page_text') if rows and isinstance(rows[0].get('metadata'), dict) else None
    return text.split('\n') if isinstance(text, str) and text else None


def sync(store, config, account, helpers):
    try:
        url = address(account.get('url'))
    except ValueError:
        raise helpers.SourceError('web_page_address') from None
    state = store.checkpoint(account['id']) or {}
    if time.time() - float(state.get('read_at') or 0) < MIN_SECONDS:
        return {'mode': 'incremental', 'events': 0}  # read within the hour: never sooner, whatever asked
    state['read_at'] = time.time()
    status, title, lines = read(url, state, helpers.SourceError)
    if status == 304 or fingerprint(lines) == state.get('hash'):
        store.commit_page(account['id'], state, [])
        return {'mode': 'incremental', 'events': 0}
    before = baseline(store, account) if state.get('hash') else None
    state['hash'] = fingerprint(lines)
    if before is None:  # the first read: what it says now is the baseline, kept as reviewed, never a signal of its own
        store.commit_page(account['id'], state, [{**event(account, url, title, '\n'.join(lines[:30]), lines, helpers.now()), 'reviewed': True}])
        return {'mode': 'incremental', 'events': 0}
    body = changes(before, lines)
    if not body:  # nothing to show beyond dates and times: not a signal
        store.commit_page(account['id'], state, [])
        return {'mode': 'incremental', 'events': 0}
    store.commit_page(account['id'], state, [event(account, url, title, body, lines, helpers.now())])
    return {'mode': 'incremental', 'events': 1}


def check(config, account, helpers):
    """Setup's read: the address is a public https page that robots.txt lets it read and that has text. Names the
    connection after the page ('example.com/pricing'). No event, no checkpoint."""
    try:
        account['url'] = address(account.get('url'))
    except ValueError:
        raise helpers.SourceError('web_page_address') from None
    account.setdefault('display_name', page_name(account['url']))
    read(account['url'], {}, helpers.SourceError)
