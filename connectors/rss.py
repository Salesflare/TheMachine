"""Example connector: an RSS or Atom feed.

Config: {"id": "work-feed", "service": "rss", "transport": "http", "boundary": "work:Acme",
         "url": "https://example.com/feed.xml", "poll_seconds": 1800}

Each read is one HTTPS GET through the Web page connector's reader (connectors/web_page.py get): only public
addresses, every redirect hop too, checked on the socket; at most MAX_BYTES (also once unpacked) in its TIMEOUT; never
more than once every MIN_SECONDS, whatever poll_seconds says; If-None-Match/If-Modified-Since when the feed gives them.

A connector is one module in connectors/ named after its service. It exposes
sync(store, config, account, helpers) and optionally KINDS (event kind -> label).
"""
import calendar
import datetime as dt
import email.utils
import hashlib
import re
import time
import xml.etree.ElementTree as ET
import zlib
from xml.parsers import expat

from connectors import web_page

UA = 'TheMachine/1 (+feed reader)'
MAX_BYTES = 5_000_000  # of a feed, also once unpacked
MIN_SECONDS = 900  # never read a feed more often than this, whatever poll_seconds says
# The reader's errors (connectors/web_page.py get) as this connector's own
READ_ERRORS = {'web_page_address': 'rss_address', 'web_page_redirects': 'rss_redirects', 'web_page_network': 'network:OSError:rss_read'}
KINDS = {'rss.item': 'feed'}
# How each kind reads in the message viewer (email, chat, notification or card) and the app its link opens in
# (machine/store/message_view.py; docs/adding-a-source.md, "How a message reads")
VIEWS = {'rss.item': 'card'}
APP = ''
# For `assistant connect rss`: the account it adds and what it asks (see docs/adding-a-source.md).
SETUP = {'label': 'RSS feed', 'what': 'Posts from the feeds you follow.',
         'account': {'id': 'feed', 'service': 'rss', 'transport': 'http', 'boundary': 'work', 'poll_seconds': 1800},
         'ask': [('url', 'Feed URL (RSS or Atom)')],
         'hints': {'rss_address': 'use a public https:// address'}}
ATOM = '{http://www.w3.org/2005/Atom}'


def parse_xml(raw):
    """ElementTree from bytes, refusing any DTD (so no entity expansion or external entities), as defusedxml does."""
    builder = ET.TreeBuilder()
    parser = expat.ParserCreate(namespace_separator='}')
    name = lambda tag: '{' + tag if '}' in tag else tag  # expat's 'ns}tag' as ElementTree's '{ns}tag'

    def refuse(*_):
        raise ET.ParseError('XML with a DTD or entities is refused')
    parser.StartDoctypeDeclHandler = parser.EntityDeclHandler = parser.ExternalEntityRefHandler = refuse
    parser.StartElementHandler = lambda tag, attrs: builder.start(name(tag), {name(k): v for k, v in attrs.items()})
    parser.EndElementHandler = lambda tag: builder.end(name(tag))
    parser.CharacterDataHandler = builder.data
    parser.buffer_text = True
    try:
        parser.Parse(raw, True)
    except expat.ExpatError as error:
        raise ET.ParseError(str(error)) from None
    return builder.close()


def fetch(url, state, SourceError):
    """One GET of the feed through the Web page connector's reader (web_page.get): public https addresses only, every
    redirect hop too, checked on the socket itself, so no feed or redirect can point it at this computer, its network
    or a cloud server's metadata address. (body, headers); body None when the feed says it didn't change (304)."""
    headers = {'User-Agent': UA, 'Accept': 'application/rss+xml, application/atom+xml, application/xml;q=0.9, text/xml;q=0.9, */*;q=0.5'}
    if state.get('etag'):
        headers['If-None-Match'] = state['etag']
    if state.get('last_modified'):
        headers['If-Modified-Since'] = state['last_modified']
    try:
        status, response, body, _ = web_page.get(url, SourceError, headers, limit=MAX_BYTES)
    except SourceError as error:
        raise SourceError(READ_ERRORS.get(error.category, error.category)) from None
    if status == 304:
        return None, response
    if status != 200:
        raise SourceError('rss_http', status, retry_after=3600 if status == 429 else None)
    if (response.get('Content-Encoding') or '').lower() == 'gzip':
        try:
            inflate = zlib.decompressobj(16 + zlib.MAX_WBITS)
            body = inflate.decompress(body, MAX_BYTES + 1)
        except zlib.error:
            raise SourceError('rss_invalid_xml') from None
        if inflate.unconsumed_tail:
            body += b'!'  # more than MAX_BYTES unpacked: too large
    return body, response


def text(node, *names):
    for name in names:
        found = node.find(name)
        if found is not None and (found.text or found.get('href')):
            return (found.text or found.get('href')).strip()
    return ''


def when(value):
    if not value:
        return None
    try:
        parsed = email.utils.parsedate_tz(value)
        if parsed:
            return calendar.timegm(parsed[:9]) - (parsed[9] or 0)
    except (TypeError, ValueError):
        pass
    match = re.fullmatch(r'(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})(?:\.\d+)?(Z|[+-]\d{2}:\d{2})', value.strip())
    if not match:
        return None
    return dt.datetime.fromisoformat(f'{match[1]}T{match[2]}{"+00:00" if match[3] == "Z" else match[3]}').timestamp()


def item_event(account, node, helpers):
    title = text(node, 'title', ATOM + 'title') or 'Untitled item'
    link = text(node, 'link', ATOM + 'link')
    guid = text(node, 'guid', ATOM + 'id') or link or title
    stamp = when(text(node, 'pubDate', ATOM + 'updated', ATOM + 'published'))
    if stamp is None:
        raise helpers.SourceError('rss_invalid_timestamp')
    body = re.sub(r'<[^>]+>', ' ', text(node, 'description', ATOM + 'summary', ATOM + 'content'))
    return {'account_id': account['id'],
            'source_id': hashlib.sha256(guid.encode()).hexdigest(),
            'kind': 'rss.item',
            'occurred_at': helpers.iso(stamp),
            'title': title[:1000],
            'body': re.sub(r'\s+', ' ', body).strip()[:40000],
            'metadata': {'source_url': link, 'feed': account['url'], 'guid': guid},
            'deleted': False}


def sync(store, config, account, helpers):
    if not re.fullmatch(r'https://\S+', account.get('url') or ''):
        raise helpers.SourceError('rss_missing_url')
    state = store.checkpoint(account['id']) or {}
    if time.time() - float(state.get('read_at') or 0) < MIN_SECONDS:
        return {'mode': 'incremental', 'events': 0}  # read within MIN_SECONDS: never sooner, whatever asked
    state['read_at'] = time.time()
    raw, headers = fetch(account['url'], state, helpers.SourceError)
    events, skipped = [], helpers.Skips('rss_invalid_item')
    if raw is not None:
        if len(raw) > MAX_BYTES:
            raise helpers.SourceError('rss_feed_too_large')
        try:
            root = parse_xml(raw)
        except ET.ParseError:
            raise helpers.SourceError('rss_invalid_xml') from None
        nodes = root.findall('./channel/item') or root.findall(ATOM + 'entry')
        # An item it can't take (no date, say) is counted, never failing the feed (helpers.Skips)
        events = list({e['source_id']: e for e, _ in skipped.every(nodes[:200], lambda n: item_event(account, n, helpers))}.values())
        skipped.check().note(state)
    state.update(etag=headers.get('ETag') or state.get('etag'),
                 last_modified=headers.get('Last-Modified') or state.get('last_modified'))
    # Unchanged items are skipped by content hash, so rereading the feed is idempotent.
    store.commit_page(account['id'], state, events)
    return {'mode': 'incremental', 'events': len(events), 'skipped': sum(skipped.values())}


def check(config, account, helpers):
    """Read-only setup probe: same fetch/parser as sync, without events or a checkpoint write."""
    if not re.fullmatch(r'https://\S+', account.get('url') or ''):
        raise helpers.SourceError('rss_missing_url')
    raw, _ = fetch(account['url'], {}, helpers.SourceError)
    if raw is None or len(raw) > MAX_BYTES:
        raise helpers.SourceError('rss_invalid_feed' if raw is None else 'rss_feed_too_large')
    try:
        root = parse_xml(raw)
    except ET.ParseError:
        raise helpers.SourceError('rss_invalid_xml') from None
    if root.tag not in ('rss', ATOM + 'feed'):
        raise helpers.SourceError('rss_invalid_feed')
    skipped = helpers.Skips('rss_invalid_item')  # as sync: a few odd items are fine, a feed of nothing but odd ones is not
    skipped.every((root.findall('./channel/item') or root.findall(ATOM + 'entry'))[:200], lambda n: item_event(account, n, helpers))
    if skipped and not skipped.taken:
        raise helpers.SourceError(skipped.most_common(1)[0][0])
