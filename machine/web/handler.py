"""The dashboard's HTTP handler (refactor PR 20): make_handler(app) returns the Handler class App.serve runs, the same
class that was nested in App.serve, with `app` the same closure. Every route, the owner and CSRF checks, the CSP and
the uploads are here. Moved out of assistant.py as is (one indent level less)."""
import email.utils
import hashlib
import hmac
import html
import http.server
import json
import mimetypes
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import time
import urllib.request

import ai_access
import browser_viewer
import chat_files
import crm
import crm_fields
import crm_import
import embeddings
import enrichment
import fleet
import graph
import locale_prefs
from machine.actions import DASHBOARD_ACTIONS, OWNER_ACTIONS, UPLOAD_ACTIONS
from machine.browser import browser_link, PANE_QUERY
from machine.config import BRAND_ASSETS, LOG, ROOT
from machine.delivery.push import app_notice, push_key
from machine.faults import source_url
from machine import omarchy
from machine.sources.calendar import calendar_account_owner, company_domains, invite_people, team_people
from machine.sources.connectors import writable_calendars
from machine.store.views import DONE_FIRST
from machine.text import _address, ATTACHMENT_INLINE, encoded, shown_body
from machine.timing import _REQUEST_TIMING, SLOW_REQUEST_SECONDS, close_kept
from machine.web import status_delta
from machine.web.serving import (
    compress_body,
    COMPRESS_MIN,
    COMPRESSIBLE,
    content_codings,
    dashboard_base,
    dashboard_cache_scope,
    dashboard_csrf,
    dashboard_hosts,
    dashboard_page,
    dashboard_script,
    dashboard_status,
    dashboard_version,
    etag_matches,
    SCRIPT_CACHE,
    SCRIPT_NAME,
    tailnet_login,
)
import meeting_notes
import next_actions
import notify
import places
import shared_graph
from sources import SourceError
from timeutil import now
import voice_input
import whatsapp_images


UPLOAD_REQUEST_BYTES = 9 * 1024 * 1024


# What the dashboard says when an action fails on something other than a ValueError (which says what to do itself)
ACTION_FAILED = 'That didn’t go through. Reload the page and try again.'


# Email, whatever brought it in: what New to-do's Email pill searches (api/events?kind=email)
EMAIL_KINDS = frozenset({'gmail.message', 'ms_graph.message', 'outlook.message', 'salesflare.email', 'fleet.email'})


def browser_embed(config, host=''):
    """The viewer on the dashboard's own address, for the dashboard to show it in its main area on a computer, or
    None: with `browser_vnc` the dashboard's own /browser; on a hosted Machine (its browser_url is the control plane's
    handoff) the Machine's /browser/, which its proxy serves from the viewer files once they have the short page. There
    the browser takes the pane's own size (resize=remote, as on a phone), so it fills the pane without black bars."""
    if config.get('browser_vnc') and config.get('dashboard_host'):
        return browser_viewer.view_link(dashboard_base(config, host), config.get('browser_novnc') or browser_viewer.WEB)
    url = urllib.parse.urlsplit(str(config.get('browser_url') or ''))
    web = Path(config.get('browser_novnc') or browser_viewer.WEB).expanduser()
    if url.scheme == 'https' and url.path == '/open' and url.query == 'to=browser' and (web / 'index.html').is_file():
        return '/browser/?' + PANE_QUERY
    return None


MAIL_HEAD = re.compile(r'(?:(?:From|To|Cc|Date|Subject): [^\n]*\n)+\s*')


SLACK_LINK = re.compile(r'<(https?://[^|>]+)(?:\|([^>]+))?>')


def event_glance(event, accounts, own=(), chars=240):
    """An event as a row in the Graph shows it: who wrote it (You for the owner, also from another address of theirs:
    own) and the start of its text, in one line."""
    m = event.get('metadata') or {}
    account = next((a for a in accounts if a.get('id') == event.get('account_id')), {})
    mine = bool(m.get('from_me')) or 'SENT' in (m.get('labels') or ()) or (
        event.get('kind') == 'slack.message' and bool(m.get('user_id')) and m.get('user_id') == account.get('user_id')) or (
        event.get('kind') == 'gmail.message' and _address(m.get('from')) in own)
    sender = str(m.get('sender_display') or m.get('from') or '')
    who = 'You' if mine else (email.utils.parseaddr(sender)[0] or sender if '@' in sender else sender)
    text = shown_body(event.get('body'))[0]
    if event.get('kind') == 'calendar.event':
        text = ' · '.join(v for v in (str(m.get('location') or ''), text) if v)
    text = SLACK_LINK.sub(lambda g: g.group(2) or g.group(1), MAIL_HEAD.sub('', text, count=1) if text.startswith('From: ') else text)
    text = ' '.join(text.split())
    out = {'from': who[:80] or None, 'from_me': mine, 'preview': text[:chars] + ('…' if len(text) > chars else '')}
    if event.get('kind') == 'slack.message':  # a direct message, or the channel it was said in
        out['dm'] = m.get('conversation_type') == 'dm'
        if not out['dm'] and m.get('channel_name'):
            out['place'] = '#' + str(m['channel_name'])[:80]
    # The conversation a chat message is part of, so the Graph shows a run of them as one row. Mail and meetings: none.
    thread = {'whatsapp.message': m.get('chat_id'), 'telegram.message': m.get('chat_id'), 'teams.message': m.get('chat_id'), 'slack.message': m.get('channel_id'), 'linkedin.message': m.get('conversation_id'),
              'x.dm': m.get('conversation_id'), 'intercom.conversation': m.get('conversation_id')}.get(event.get('kind'))
    if thread:
        out['thread'] = f"{event.get('account_id')}:{event.get('kind')}:{thread}"
    return out


def approval_document(proposal):
    # A reviewer-only page, not an approval endpoint or a general file reader.
    title, detail = html.escape(proposal['title']), html.escape(proposal['detail'])
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · The Machine</title><style>
body{{background:#202329;color:#eee9d6;font:17px system-ui;margin:0;padding:20px;line-height:1.5}}
main{{max-width:900px;margin:auto}}h1{{font-size:24px}}pre{{background:#292c33;padding:16px;border-radius:12px;white-space:pre-wrap;overflow-wrap:anywhere;font-size:14px}}
</style></head><body><main><h1>{title}</h1><p>Review the complete change below. Return to Telegram to allow it once or deny it. Nothing runs from this page.</p>
<pre>{detail}</pre></main></body></html>'''


def make_handler(app):
    """The Handler class for the dashboard server of this App (the closure App.serve had)."""
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass  # Access URLs/searches can contain private information.

        def send_response(self, *args, **kwargs):
            self.answered = True
            super().send_response(*args, **kwargs)

        def parse_request(self):
            # the request line is in: the clock starts here, not while a kept-alive connection waits for the next one
            self.started, self.action_name = time.monotonic(), ''
            close_kept(getattr(_REQUEST_TIMING, 'value', None))  # a request before it on this thread that wasn't logged
            _REQUEST_TIMING.value = {'db_wait': 0.0, 'db_held': 0.0, 'db_connections': 0}
            ok = super().parse_request()
            _REQUEST_TIMING.value['read'] = ok and self.command == 'GET'  # a read: what it reads twice can be kept (Fleet.meta)
            return ok

        def handle_one_request(self):
            """An unexpected error answers a plain 500 with its reason instead of dropping the connection: a proxy in
            front (Caddy) reads a dropped answer as the service restarting and says so. The traceback goes to the log."""
            self.answered, self.started = False, None
            try:
                self.answer_one_request()
            finally:
                self.log_slow()

        def log_slow(self):
            """A request over SLOW_REQUEST_SECONDS: its path (no query), the action, the total and the database time."""
            timing, _REQUEST_TIMING.value = getattr(_REQUEST_TIMING, 'value', None), None
            close_kept(timing)  # the connections it kept between its store.connect calls
            if self.started is None or timing is None:
                return
            total = time.monotonic() - self.started
            if total < SLOW_REQUEST_SECONDS:
                return
            path = urllib.parse.urlsplit(getattr(self, 'path', '') or '').path[:80]
            LOG.warning('slow request method=%s path=%s action=%s total=%.1fs db_wait=%.1fs db_held=%.1fs db_connections=%d',
                        self.command, path, self.action_name or '-', total, timing['db_wait'], timing['db_held'],
                        timing['db_connections'])

        def answer_one_request(self):
            try:
                super().handle_one_request()
            except Exception as error:
                if isinstance(error, (BrokenPipeError, ConnectionResetError)):
                    raise
                LOG.exception('request failed path=%s', urllib.parse.urlsplit(getattr(self, 'path', '') or '').path)
                self.close_connection = True
                if not self.answered and getattr(self, 'path', None):
                    try:
                        self.output(500, {'error': 'Something went wrong on your Machine. Try again.'})
                        self.wfile.flush()
                    except Exception:  # the connection itself is gone: nothing more to say
                        pass

        def coding(self, data, content_type, status=200):
            """The coding for this answer (compressed answers, COMPRESSIBLE): None when it goes as it is."""
            if (status != 200 or self.command != 'GET' or urllib.parse.urlsplit(self.path).path not in COMPRESSIBLE or
                    len(data) < COMPRESS_MIN or not (content_type.startswith('text/') or content_type.endswith('json') or
                                                     content_type.endswith('javascript'))):
                return None
            return next(iter(content_codings(self.headers.get('Accept-Encoding'))), None)

        def output(self, status, value, content_type='application/json', packed=None, referrer='no-referrer', cache='no-store'):
            """`packed`: the answer already compressed, as (coding, bytes), for the page (kept per release). `referrer`:
            the consent page's is same-origin, since under no-referrer Chrome sends its form's POST with `Origin: null`."""
            data = value if isinstance(value, bytes) else encoded(value).encode() if content_type == 'application/json' else value.encode()
            coding = packed[0] if packed else self.coding(data, content_type, status)
            if coding:
                data = packed[1] if packed else compress_body(data, coding)
            self.send_response(status)
            self.send_header('Content-Type', content_type if content_type.startswith('image/') or content_type=='application/pdf' else content_type + '; charset=utf-8')
            self.send_header('Cache-Control', cache)
            if coding or urllib.parse.urlsplit(self.path).path in COMPRESSIBLE:
                self.send_header('Vary', 'Accept-Encoding')
            if coding:
                self.send_header('Content-Encoding', coding)
            self.send_header('Content-Length', str(len(data)))
            if getattr(self, 'etag', None):
                # One ETag per coding (a strong ETag names the bytes sent); If-None-Match matches any of them
                self.send_header('ETag', self.etag[:-1] + '-' + coding + '"' if coding else self.etag)
                self.etag = None
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', referrer)
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' https: data:; font-src 'self' https: data:; frame-ancestors 'none'")
            self.end_headers()
            try:
                self.wfile.write(data)
            except (BrokenPipeError, ConnectionResetError):
                self.close_connection = True  # client went away; nothing to log

        timeout = app.config.get('http_timeout', 15)  # a stalled client cannot hold a thread forever

        def internal(self):
            return hmac.compare_digest(self.headers.get('Authorization', '').encode(), ('Bearer ' + app.token).encode())

        def owner(self):
            # Tailscale Serve (:8443) sends the login; Caddy (:443) sends the peer address instead.
            # On TLS early-data (0-RTT) requests Caddy leaves {remote_host} empty but still sets
            # X-Forwarded-For itself (it drops untrusted incoming values), so fall back to that.
            peer = self.headers.get('X-Tailnet-Client')
            if peer == '':
                peer = self.headers.get('X-Forwarded-For', '').split(',')[-1].strip()
            peer = peer or ''
            login = tailnet_login(peer) if peer else self.headers.get('Tailscale-User-Login', '')
            ok = (self.client_address[0] == '127.0.0.1' and login == app.config['tailscale_owner'] and
                  self.headers.get('Host', '') in dashboard_hosts(app.config))
            if not ok and not self.internal():
                print(f"dashboard refused: host={self.headers.get('Host', '')!r} peer={peer!r} login={login!r} path={self.path.split('?')[0]!r}", file=sys.stderr, flush=True)
            return ok

        def ai(self, method):
            """/mcp, /oauth/token, /oauth/register, /oauth/revoke and the OAuth metadata (ai_app.py): a connected AI's own
            token or key, never the owner's sign-in or the service's token. Nothing about the request is logged."""
            try:
                length = int(self.headers.get('Content-Length') or 0) if method == 'POST' else 0
            except ValueError:
                length = -1
            if not 0 <= length <= ai_access.BODY_MAX:
                self.close_connection = True
                self.output(413, {'error': 'Too big'})
                return
            try:
                body = self.rfile.read(length) if length else b''
            except OSError:
                self.close_connection = True
                return
            status, headers, data = app.ai_http(method, urllib.parse.urlsplit(self.path).path, self.headers, body, self.headers.get('Host', ''))
            self.send_response(status)
            for name, value in headers.items():
                self.send_header(name, value)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.end_headers()
            try:
                self.wfile.write(data)
            except (BrokenPipeError, ConnectionResetError):
                self.close_connection = True

        def do_DELETE(self):
            if urllib.parse.urlsplit(self.path).path == '/mcp':
                self.ai('DELETE')
            else:
                self.output(405, {'error': 'Not allowed'})

        def do_GET(self):
            path = urllib.parse.urlsplit(self.path)
            if path.path == '/health':
                self.output(200, {'ok': True})
                return
            if path.path in ai_access.PUBLIC_GET:
                self.ai('GET')
                return
            if not self.owner():
                if path.path == ai_access.AUTHORIZE:  # a person in a browser, mid sign-in: a page, never JSON
                    self.output(403, ai_access.refused_page('signin', lang=locale_prefs.language()), 'text/html')
                    return
                self.output(403, {'error': 'Use the owner-authenticated Tailscale dashboard'})
                return
            if (path.path == '/browser' or path.path.startswith('/browser/')) and app.config.get('browser_vnc'):
                self.browser_view(path.path[len('/browser/'):], short=path.path in ('/browser', '/browser/'))
            elif path.path == '/':
                page = dashboard_page(app.token, app.config['tailscale_owner'], dashboard_base(app.config, self.headers.get('Host', '')))
                page = dashboard_script(page)[0]  # its main script is a file of its own (/app-<hash>.js, below)
                # The installed app's service worker keeps a copy of this page and asks again with its ETag: an
                # unchanged page is a short 304 instead of the whole page over a phone's connection.
                etag = '"' + hashlib.sha256(page.encode()).hexdigest()[:24] + '"'
                coding = self.coding(page.encode(), 'text/html')
                if etag_matches(self.headers.get('If-None-Match'), etag):
                    self.send_response(304)
                    self.send_header('ETag', etag[:-1] + '-' + coding + '"' if coding else etag)
                    self.send_header('Vary', 'Accept-Encoding')
                    self.send_header('Cache-Control', 'no-store')
                    self.end_headers()
                    return
                self.etag = etag
                self.output(200, page, 'text/html', packed=coding and app.packed_page(etag, coding, page))
            elif path.path == ai_access.AUTHORIZE:  # a connected AI's sign-in: the owner's own consent page (ai_app.py)
                status, page = app.ai_consent_page(path.query, dashboard_csrf(app.token, app.config['tailscale_owner']))
                if status == 303:
                    self.send_response(303)
                    self.send_header('Location', page)
                    self.send_header('Cache-Control', 'no-store')
                    self.send_header('Content-Length', '0')
                    self.end_headers()
                else:
                    self.output(status, page, 'text/html', referrer='same-origin')
            elif SCRIPT_NAME.fullmatch(path.path):
                # The page's main script (dashboard_script): kept by the browser for a year under its name, which changes
                # with it. A name from another release (a page kept by an older service worker) gets this release's
                # script, not kept: the page then sees the new release and loads it.
                _, name, script = dashboard_script(dashboard_page(app.token, app.config['tailscale_owner'], '/'))
                if not name:
                    self.output(404, {'error': 'Not found'})
                    return
                data = script.encode()
                coding = len(data) >= COMPRESS_MIN and next(iter(content_codings(self.headers.get('Accept-Encoding'))), None)
                self.output(200, data, 'text/javascript', packed=coding and app.packed_page('"' + name + '"', coding, script),
                            cache=SCRIPT_CACHE if path.path == '/' + name else 'no-store')
            elif path.path == '/manifest.webmanifest':
                self.output(200, (ROOT / 'manifest.webmanifest').read_text(), 'application/manifest+json')
            elif path.path == '/sw.js':
                self.output(200, (ROOT / 'sw.js').read_text(), 'text/javascript')
            elif re.fullmatch(r'/i18n/[a-z]{2}(?:-[A-Z]{2})?\.json', path.path) and path.path[6:-5] in locale_prefs.LANGUAGES:
                self.output(200, (ROOT / 'i18n' / path.path[6:]).read_bytes(), 'application/json')  # the catalogs (i18n.py)
            elif path.path == '/api/push-key':
                self.output(200, {'key': push_key(app.config)})
            elif path.path == '/api/omarchy-theme':  # this computer's Omarchy colors, or {} without Omarchy (machine/omarchy.py)
                # The browser's own address as the proxy in front saw it (as owner() reads it); no proxy header: direct.
                peer = self.headers.get('X-Tailnet-Client')
                if not peer:
                    peer = self.headers.get('X-Forwarded-For', '').split(',')[-1].strip() or (None if peer == '' or self.headers.get('Tailscale-User-Login') else '')
                here = omarchy.same_host(peer)
                etag = omarchy.tag(here=here)
                if etag and etag_matches(self.headers.get('If-None-Match'), etag):  # asked every 2 s: a stat until the theme changes
                    self.send_response(304)
                    self.send_header('ETag', etag)
                    self.send_header('Cache-Control', 'no-store')
                    self.end_headers()
                    return
                current = omarchy.theme()
                self.etag = etag if current else None
                self.output(200, {**current, 'here': here} if current else {})
            elif path.path in BRAND_ASSETS:
                asset = BRAND_ASSETS[path.path]
                self.output(200, asset.read_bytes(), {'.webp': 'image/webp', '.woff2': 'font/woff2', '.mp3': 'audio/mpeg'}.get(asset.suffix, 'image/png'))
            elif path.path == '/api/session':
                # Asked once by a page: the CSRF token (a page started from the app's on-device copy has none, that
                # copy never keeps it) and whose data the device may keep (dashboard_cache_scope)
                app.store.note_activity('visit')
                self.output(200, {'csrf': dashboard_csrf(app.token, app.config['tailscale_owner']),
                                  'cache_scope': dashboard_cache_scope(app.token, app.config['tailscale_owner'])})
            elif path.path == '/api/notice':
                # The mobile app, woken by a push without text: what its notification says and which buttons it
                # gets (app_notice), over the owner's own sign-in, so no to-do text passes through the push
                query = urllib.parse.parse_qs(path.query)
                tag, kind = (query.get('tag') or [''])[0], (query.get('kind') or [''])[0]
                version = 2 if (query.get('v') or [''])[0] == '2' else 1  # an app with the quick buttons (QUICK)
                self.output(200, app_notice(app.store, app.config, tag, kind if kind in notify.KINDS else None, version))
            elif path.path == '/api/status':
                since = (urllib.parse.parse_qs(path.query).get('since') or [''])[0]
                self.output(200, status_delta.changes({**dashboard_status(app.action('status', {'full': True, 'done': DONE_FIRST})), 'talk_ready': app.talk_ready(), 'ui_version': dashboard_version(), 'source_url': source_url(), 'meaning': {'on': bool(embeddings.settings(app.config))}, 'fixed': list(getattr(getattr(app, 'fleet', None), 'fixed_now', None) or ()), 'browser_link': browser_link(app.config),
                                  'browser_embed': browser_embed(app.config, self.headers.get('Host', ''))}, since))
                try:
                    app.store.note_card_shown()
                    app.store.note_activity('dashboard')
                except sqlite3.Error as error:
                    LOG.warning('card shown not noted error=%s', type(error).__name__)
            elif path.path == '/api/merge-diff':
                args=urllib.parse.parse_qs(path.query)
                try:
                    with app.store.connect() as db:
                        row=db.execute('SELECT next_action FROM suggestions WHERE id=?',(args.get('id',[''])[0],)).fetchone()
                    action=next_actions.selected(row['next_action'],args.get('revision',[''])[0]) if row else None
                    if not action:raise ValueError('Merge proposal not found')
                    self.output(200,next_actions.full_merge_diff(action),'text/plain')
                except (ValueError,OSError,subprocess.TimeoutExpired):
                    self.output(404,{'error':'The complete diff for this proposal is not available'})
            elif path.path == '/approval':
                try:
                    proposal_id = urllib.parse.parse_qs(path.query).get('id', [''])[0]
                    proposal = app.store.tool_approval_document(proposal_id)
                    self.output(200, approval_document(proposal), 'text/html')
                except (ValueError, sqlite3.OperationalError):
                    self.output(404, {'error': 'Approval proposal not found'})
            elif path.path == '/api/events':
                args = urllib.parse.parse_qs(path.query)
                try:
                    query = args.get('q', [''])[0]
                    # With words, search by meaning and keywords together; "all" searches every account. kind=email:
                    # emails only, by keywords (New to-do's Email pill: subjects and senders, at once).
                    email = args.get('kind', [''])[0] == 'email'
                    rows = app.action('events', {'account_ids': args.get('account', []), 'query': query, 'semantic': bool(query.strip()) and not email,
                                                 'full': True, **({'kinds': sorted(EMAIL_KINDS)} if email else {})})
                    self.output(200, [{**r, 'body': whatsapp_images.listed(shown_body(r.get('body'))[0])} for r in rows])  # read by people: no model marker
                except (ValueError, sqlite3.OperationalError):
                    self.output(400, {'error': 'Select accounts and use a valid search'})
            elif path.path == '/api/account':
                self.output(200, app.account_view())
            elif path.path == '/api/activity':  # Settings, Activity: everything The Machine did, a page at a time (activity_log.py)
                args = {k: v[0] for k, v in urllib.parse.parse_qs(path.query).items()}
                try:
                    self.output(200, app.activity_view(args.get('kind', ''), args.get('cursor') or 0, args.get('outcome', ''), args.get('actor', '')))
                except (ValueError, sqlite3.OperationalError):
                    self.output(400, {'error': 'Not an activity page'})
            elif path.path == '/api/calendar':  # the Calendar tab: meetings in a window, and the calendars it can add to
                args = urllib.parse.parse_qs(path.query)
                try:
                    owner = app.owner_emails()
                    writable = writable_calendars(app.config)
                    self.output(200, {'meetings': app.store.calendar([a['id'] for a in app.config['accounts']],
                                                                     args.get('from', [''])[0], args.get('to', [''])[0], owner,
                                                                     {c['id'] for c in writable},
                                                                     {a['id']: n for a in app.config['accounts'] if (n := calendar_account_owner(a))}),
                                      'calendars': writable, 'starts': app.calendar_starts()})  # where its meetings begin: the line at the edge
                except (ValueError, sqlite3.OperationalError):
                    self.output(400, {'error': 'Ask for a window of at most 15 days'})
            elif path.path == '/api/meeting':  # one meeting as the Calendar shows it, opened from anywhere in the dashboard
                args = urllib.parse.parse_qs(path.query)
                try:
                    writable = writable_calendars(app.config)
                    self.output(200, {'meeting': app.store.meeting([a['id'] for a in app.config['accounts']], int(args.get('event', [''])[0]),
                                                                   app.owner_emails(), {c['id'] for c in writable},
                                                                   {a['id']: n for a in app.config['accounts'] if (n := calendar_account_owner(a))})})
                except (ValueError, sqlite3.OperationalError):
                    self.output(400, {'error': 'That meeting is not there anymore'})
            elif path.path == '/api/meeting-notes':  # a meeting's notes in the Calendar: added ones and Zoom's, read only
                args = urllib.parse.parse_qs(path.query)
                try:
                    self.output(200, app.meeting_notes({'event_id': args.get('event', [''])[0] or None}, True, meeting_notes.MAX_CHARS))
                except (ValueError, sqlite3.OperationalError):
                    self.output(400, {'error': 'That meeting is not there anymore'})
            elif path.path == '/api/places':  # the Calendar form's Where: the owner's places first, then the map
                args = urllib.parse.parse_qs(path.query)
                with app.store.connect() as db:
                    self.output(200, {'places': places.suggest(db, app.config, args.get('q', [''])[0][:200])})
            elif path.path == '/api/invitees':  # the Calendar form's Invite: people from the owner's Graph
                with app.store.connect() as db:
                    query = urllib.parse.parse_qs(path.query)
                    typed = query.get('q', [''])[0][:200]
                    self.output(200, {'people': team_people(db, typed, app.owner_emails(), company_domains(app.config), app.teammate_addresses()) if query.get('team')
                                      else invite_people(db, typed, app.owner_emails())})
            elif path.path == '/api/fleet':
                if not getattr(app, 'fleet', None):
                    self.output(200, {'on': False})
                else:
                    try:
                        if urllib.parse.parse_qs(path.query).get('refresh'):
                            app.fleet.directory(refresh=True)
                    except (fleet.Off, ValueError, OSError):
                        pass
                    self.output(200, app.fleet_view())
            elif path.path == '/api/promise':  # a promise's own page: read-only
                try:
                    found = app.store.promise_page(int(urllib.parse.parse_qs(path.query).get('id', [''])[0]))
                    rows = app.store.events([a['id'] for a in app.config['accounts']], event_ids=[found['event_id']])
                    found['source'] = [{'id': r['id'], 'account_id': r['account_id'], 'kind': r['kind'], 'occurred_at': r['occurred_at'], 'title': r['title'][:200],
                                        'source_url': r['metadata'].get('source_url'), **event_glance(r, app.config['accounts'], app.owner_emails())} for r in rows][:1]
                    self.output(200, found)
                except (ValueError, sqlite3.OperationalError):
                    self.output(404, {'error': 'No such promise'})
            elif path.path == '/api/graph/follow-ups':  # "Follow-ups on", "Next follow-up: Thu": after the board, which they held up
                with app.store.connect() as db:
                    self.output(200, app.follow_up_board_views(db))
            elif path.path in ('/api/graph/list', '/api/cards/done'):  # the long lists, a page at a time
                args = {k: v[0] for k, v in urllib.parse.parse_qs(path.query).items()}
                try:
                    if path.path == '/api/cards/done':
                        self.output(200, app.store.done_page(args.get('cursor') or 0, args.get('limit') or 30, args.get('q', ''), args.get('scope', ''), args.get('id', '')))
                    elif args.get('ids') == '1':  # the ids its filters keep, for the Projects board
                        self.output(200, app.graph_list_ids(args.get('list', ''), {k: args[k] for k in crm.FILTERS if k in args}))
                    else:
                        self.output(200, app.graph_list(args.get('list', ''), args.get('sort', ''), args.get('cursor') or 0, args.get('limit') or 30,
                                                        {k: args[k] for k in crm.FILTERS if k in args}))
                except (ValueError, sqlite3.OperationalError):
                    self.output(400, {'error': 'Not a list'})
            elif path.path == '/api/graph/timeline':  # a person's or organization's timeline, a page and a source at a time
                args = {k: v[0] for k, v in urllib.parse.parse_qs(path.query).items()}
                try:
                    if str(args.get('node', '')).startswith('team:'):
                        raise ValueError('not on the team Graph')
                    self.output(200, app.graph_timeline(args.get('node', ''), args.get('source', ''), args.get('cursor') or 0, args.get('limit') or 40))
                except (ValueError, sqlite3.OperationalError):
                    self.output(404, {'error': 'Not in the graph'})
            elif path.path == '/api/graph':
                node = urllib.parse.parse_qs(path.query).get('node', [''])[0]
                query = urllib.parse.parse_qs(path.query).get('q', [''])[0]
                try:
                    params = urllib.parse.parse_qs(path.query)
                    view, team_node, thread = params.get('view', [''])[0], node.startswith('team:'), params.get('thread', [''])[0]
                    if thread and app.fleet:  # a client thread a teammate shared, in full
                        with app.store.connect() as db:
                            self.output(200, app.fleet.team_thread(db, thread))
                    elif view == 'shared' and app.fleet:  # What's shared: counts, lists and the first share's look-over
                        self.output(200, app.fleet.graph_overview(params.get('fleet', [''])[0]))
                    elif view == 'held' and app.fleet:  # this week's held-back threads, from the weekly report
                        with app.store.connect() as db:
                            self.output(200, {'held': app.fleet.held_back(db)})
                    elif team_node and app.fleet:
                        with app.store.connect() as db:
                            self.output(200, app.fleet.team_detail(db, node))
                    elif view == 'team' and app.fleet and not query.strip():
                        mine = app.graph_action({'limit': 15})
                        with app.store.connect() as db:
                            found = app.fleet.team_overview(db, mine)
                            found['held'] = app.fleet.held_back(db)
                        found.update(whos_who=mine.get('whos_who'), waiting=mine.get('waiting'), warmup=[])
                        self.output(200, found)
                    elif view == 'projects':  # open projects to put a to-do on (the project picker on a to-do)
                        with app.store.connect() as db:
                            self.output(200, {'projects': graph.project_choices(db)})
                    elif query.strip():
                        self.output(200, app.graph_find(query, urllib.parse.parse_qs(path.query).get('cursor', ['0'])[0] or 0))
                    elif node and app.about_you_node(node):  # the owner's own record, also by one of their addresses
                        self.output(200, {**app.about_you(), 'can_share': app.contact_shareable()})  # Share my contact
                    elif node and params.get('part', [''])[0] == 'head':  # the record's head first; its timeline comes with the whole page
                        found = app.graph_action({'node_id': node, 'limit': 10, 'events': 1})
                        found.update(owners=app.owner_choices(), recent=[], head_only=True)
                        self.output(200, found)
                    elif node:
                        # a run of chat messages is one row; the event ids only (lines: False), as the timeline below shows them
                        found = app.graph_action({'node_id': node, 'limit': 10, 'events': 120, 'lines': False})
                        found['owners'] = app.owner_choices()
                        rows = app.store.events([a['id'] for a in app.config['accounts']], event_ids=[int(i) for i in found['recent']])
                        # The timeline: every source, newest first, a page at a time (/api/graph/timeline for the next)
                        found['timeline'] = app.graph_timeline(found['id'])
                        found['recent'] = found['timeline'].pop('items')
                        found['slack_links'] = app.slack_links(found)
                        if found.get('kind') == 'project':  # its follow-ups: on or not, the next one, what went out (follow_ups.py)
                            try:
                                with app.store.connect() as db:
                                    found['follow_up'] = app.follow_up_project(db, found['id'])
                            except (sqlite3.Error, ValueError, KeyError, TypeError) as error:
                                LOG.info('follow-up detail error=%s', type(error).__name__)
                        if app.fleet and found.get('kind') == 'person':  # sharing a contact (contact_share.py)
                            try:
                                with app.store.connect() as db:
                                    found['shared_by'] = app.fleet.contact_mark(db, found['id'])
                                found['can_share'] = app.contact_shareable()
                            except (fleet.Off, sqlite3.Error, OSError, ValueError, KeyError, TypeError) as error:
                                LOG.info('contact share detail error=%s', type(error).__name__)
                        if app.fleet:  # the Shared Graph: Keep private, what teammates know
                            try:
                                with app.store.connect() as db:
                                    labels = app.fleet.thread_labels(db, rows)
                                    if labels or any(r.get('share') for r in found['recent']) or app.fleet.is_private(db, node):
                                        found['keep_private'] = app.fleet.is_private(db, node)
                                        found['shared_with_team'] = app.fleet.record_shared(db, node)
                                    found['team'] = app.fleet.team_for(db, node)[1]
                            except (sqlite3.Error, ValueError, KeyError, TypeError) as error:
                                LOG.info('shared graph detail error=%s', type(error).__name__)
                        self.output(200, found)
                    else:
                        found = app.graph_action({'limit': 15})
                        with app.store.connect() as db:
                            found['boards'] = graph.boards(db, now())  # the Projects board view
                            found['board_suggestions'] = graph.board_suggestions(db)  # "Start a board for …?", saved by the owner or not
                            found['project_names'] = [{'id': 'project:' + str(r['id']), 'name': r['name'], 'board_id': r['board_id']} for r in db.execute(
                                'SELECT id,name,board_id FROM projects WHERE closed_at IS NULL ORDER BY name COLLATE NOCASE LIMIT 2000')]  # the board editor's picker
                            found['person_names'] = [{'id': r['id'], 'name': r['name']} for r in db.execute(
                                "SELECT id,name FROM graph_nodes WHERE kind='person' AND name<>'' ORDER BY strength DESC LIMIT 1500")]  # the project dialog's people picker
                            found['org_doubles'] = crm.org_doubles(db, 12)  # "Same organization?"
                            found['last_import'] = crm_import.last(db)  # "Undo last import"
                            found['crm_fields'] = crm_fields.fields(db)  # the owner's own fields per record type
                            found['tags'] = crm_fields.tags_in_use(db)  # for the filter sheet
                            found['currency'] = app.currency()  # project values are in it
                            if app.fleet:
                                try:  # contacts teammates, friends and Family shared here, waiting for Add or Dismiss (contact_share.py)
                                    found['contacts_in'] = app.fleet.contacts_in()
                                except (sqlite3.Error, ValueError, KeyError, TypeError) as error:
                                    LOG.info('contacts in error=%s', type(error).__name__)
                                try:
                                    found['sharing'] = app.fleet.sharing()  # the Shared Graph: Mine or Team, and when sharing starts
                                    names = app.fleet.member_names()
                                    shared_graph.ensure(db)
                                    for b in found['boards']:  # who a board is shared with by name (Share board…)
                                        b['shared_with'] = [{'fleet': f, 'member': m, 'name': names.get((f, m), 'A teammate')}
                                                            for f, m in shared_graph.shared_with(db, 'board', b['id'])] if b['visibility'] == 'people' else []
                                    found['teammates'] = [{'fleet': f, 'member': m, 'name': name} for (f, m), name in
                                                          sorted(app.fleet.graph_teammates().items(), key=lambda x: x[1].lower())]
                                except (sqlite3.Error, ValueError, KeyError, TypeError):
                                    pass
                        found['owners'] = app.owner_choices()  # who can own a record: the Work Fleet
                        self.output(200, found)
                except (ValueError, sqlite3.OperationalError):
                    self.output(404, {'error': 'Not in the graph'})
            elif path.path == '/api/knowledge-export':  # Knowledge for another AI, downloaded once (machine/app/knowledge_export.py)
                app.knowledge_download(self, urllib.parse.parse_qs(path.query).get('token', [''])[0])
            elif path.path == '/api/agent-jobs':  # polled while a Claude Code or Codex job runs: small, unlike /api/status
                self.output(200, app.agents.live() if getattr(app, 'agents', None) else {'jobs': {}})
            elif path.path in ('/api/agent-diff', '/api/agent-file'):
                args = urllib.parse.parse_qs(path.query)
                try:
                    if not getattr(app, 'agents', None):
                        raise ValueError('off')
                    if path.path == '/api/agent-diff':
                        self.output(200, app.agents.diff(args.get('job', [''])[0]), 'text/plain')
                        return
                    found = app.agents.file(args.get('job', [''])[0], args.get('path', [''])[0])
                    data = found.read_bytes()
                except (ValueError, OSError):
                    self.output(404, {'error': 'Not available'})
                    return
                mime = mimetypes.guess_type(found.name)[0] or 'application/octet-stream'
                inline = mime in ATTACHMENT_INLINE or mime in ('text/plain', 'text/markdown', 'text/csv')
                self.send_response(200)
                self.send_header('Content-Type', (mime + ('; charset=utf-8' if mime.startswith('text/') else '')) if inline else 'application/octet-stream')
                self.send_header('Content-Disposition', ('inline' if inline else 'attachment') + "; filename*=UTF-8''" + urllib.parse.quote(found.name))
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Cache-Control', 'no-store')
                self.send_header('X-Content-Type-Options', 'nosniff')
                self.send_header('Referrer-Policy', 'no-referrer')
                self.send_header('Content-Security-Policy', "default-src 'none'; img-src 'self'; style-src 'unsafe-inline'; frame-ancestors 'none'" + ('' if mime == 'application/pdf' else '; sandbox'))
                self.end_headers()
                try:self.wfile.write(data)
                except (BrokenPipeError, ConnectionResetError):self.close_connection = True
            elif path.path == '/api/person-photo':  # a looked-up photo, saved on this Machine (enrichment.photos_step)
                with app.store.connect() as db:
                    found = enrichment.photo(db, urllib.parse.parse_qs(path.query).get('p', [''])[0])
                if not found:
                    self.output(404, {'error': 'Not available'})
                    return
                self.send_response(200)
                self.send_header('Content-Type', found[1])
                self.send_header('Content-Length', str(len(found[0])))
                self.send_header('Cache-Control', 'private, max-age=86400')
                self.send_header('X-Content-Type-Options', 'nosniff')
                self.send_header('Content-Security-Policy', "default-src 'none'; sandbox")
                self.end_headers()
                try:self.wfile.write(found[0])
                except (BrokenPipeError, ConnectionResetError):self.close_connection = True
            elif path.path == '/api/reviews/live':  # polled while a review runs: small, unlike /api/status
                self.output(200, app.review_live())
            elif path.path == '/api/progress':
                try:
                    self.output(200, app.preparation_progress(urllib.parse.parse_qs(path.query).get('id', [''])[0]))
                except (ValueError, sqlite3.OperationalError):
                    self.output(404, {'error': 'Progress not available'})
            elif path.path == '/api/browser-now':  # the note in the browser's own viewer: what it is doing now
                self.output(200, {**app.browser_now(), 'lang': locale_prefs.language()})  # lang: the viewer's own words
            elif path.path == '/api/peek':  # the live look at a preparing card's browser tab
                try:
                    self.output(200, app.preparation_peek(urllib.parse.parse_qs(path.query).get('id', [''])[0]))
                except (ValueError, sqlite3.OperationalError):
                    self.output(404, {'error': 'Not available'})
            elif path.path == '/api/originals':
                try:
                    args = urllib.parse.parse_qs(path.query)
                    events = [int(v) for v in args.get('events', [''])[0].split(',') if v.strip()][:60]  # one conversation from the Graph
                    card = args.get('id', [''])[0]
                    if card and args.get('before', [''])[0]:  # Show earlier: older messages of the to-do's own conversation
                        self.output(200, {'around': app.message_context(card, int(args['before'][0]))})
                        return
                    found = {'originals': app.originals(card, args.get('event', [''])[0], events)}
                    if card:  # what was said around the to-do's source message (machine/app/conversation.py)
                        found['around'] = app.message_context_quiet(card)
                    self.output(200, found)
                except (ValueError, sqlite3.OperationalError):
                    self.output(404, {'error': 'Original not available'})
            elif path.path == '/api/email':
                args = urllib.parse.parse_qs(path.query)
                try:
                    self.output(200, app.email_view(args.get('id', [''])[0], args.get('event', [''])[0]))
                except (ValueError, StopIteration, sqlite3.OperationalError):
                    self.output(404, {'error': 'Email not available'})
                except (OSError, SourceError):  # Gmail didn't answer (network, token, rate limit): the viewer offers a retry
                    self.output(404, {'error': 'Email not available', 'retry': True})
            elif path.path in ('/api/attachment', '/api/draft-attachment', '/api/team-file'):
                args = urllib.parse.parse_qs(path.query)
                try:
                    if path.path == '/api/team-file':  # an attachment of a client thread a teammate shared (shared_graph.py)
                        if not app.fleet:
                            raise ValueError('No Fleet')
                        with app.store.connect() as db:
                            data, mime, name = app.fleet.team_file(db, args.get('thread', [''])[0], args.get('file', [''])[0])
                    elif path.path == '/api/draft-attachment':
                        data, mime, name = app.draft_attachment(args.get('id', [''])[0], args.get('sha', [''])[0])
                    else:
                        data, mime, name = app.attachment(args.get('id', [''])[0], args.get('event', [''])[0], args.get('part', [''])[0])
                except (ValueError, OSError, SourceError, StopIteration, sqlite3.OperationalError):
                    self.output(404, {'error': 'Attachment not available'})
                    return
                # Only PDFs and plain images open in the browser; anything else downloads,
                # so an attached HTML or SVG file can never run on the dashboard.
                inline = mime in ATTACHMENT_INLINE
                self.send_response(200)
                self.send_header('Content-Type', mime if inline else 'application/octet-stream')
                self.send_header('Content-Disposition', ('inline' if inline else 'attachment') + "; filename*=UTF-8''" + urllib.parse.quote(name))
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Cache-Control', 'no-store')
                self.send_header('X-Content-Type-Options', 'nosniff')
                self.send_header('Referrer-Policy', 'no-referrer')
                self.send_header('Content-Security-Policy', "default-src 'none'; img-src 'self'; style-src 'unsafe-inline'; frame-ancestors 'none'" + ('; sandbox' if mime.startswith('image/') else ''))
                self.end_headers()
                try:self.wfile.write(data)
                except (BrokenPipeError, ConnectionResetError):self.close_connection = True
            elif path.path == '/api/export-download':  # Settings, Export: the finished export (machine/app/export.py)
                app.export_download(self, path.query)
            elif path.path == '/api/chat-file':  # a file the owner added to a chat message (chat_files.py)
                try:
                    with app.store.connect() as db:
                        data, mime, name = chat_files.read(db, app.config, urllib.parse.parse_qs(path.query).get('id', [''])[0])
                except (ValueError, OSError):
                    self.output(404, {'error': 'File not available'})
                    return
                inline = mime in ATTACHMENT_INLINE  # images and PDFs open; anything else downloads
                self.send_response(200)
                self.send_header('Content-Type', mime if inline else 'application/octet-stream')
                self.send_header('Content-Disposition', ('inline' if inline else 'attachment') + "; filename*=UTF-8''" + urllib.parse.quote(name))
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Cache-Control', 'private, max-age=86400')
                self.send_header('X-Content-Type-Options', 'nosniff')
                self.send_header('Referrer-Policy', 'no-referrer')
                self.send_header('Content-Security-Policy', "default-src 'none'; img-src 'self'; style-src 'unsafe-inline'; frame-ancestors 'none'" + ('; sandbox' if mime.startswith('image/') else ''))
                self.end_headers()
                try:self.wfile.write(data)
                except (BrokenPipeError, ConnectionResetError):self.close_connection = True
            elif path.path == '/api/whatsapp-photo':  # a WhatsApp photo the Machine kept (whatsapp_images.py)
                try:
                    with app.store.connect() as db:
                        data, mime = whatsapp_images.data_of(db, app.config, urllib.parse.parse_qs(path.query).get('id', [''])[0])
                except (ValueError, OSError):
                    self.output(404, {'error': 'Photo not available'})
                    return
                self.send_response(200)
                self.send_header('Content-Type', mime)
                self.send_header('Content-Disposition', 'inline')
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Cache-Control', 'private, max-age=86400')
                self.send_header('X-Content-Type-Options', 'nosniff')
                self.send_header('Referrer-Policy', 'no-referrer')
                self.send_header('Content-Security-Policy', "default-src 'none'; img-src 'self'; frame-ancestors 'none'; sandbox")
                self.end_headers()
                try:self.wfile.write(data)
                except (BrokenPipeError, ConnectionResetError):self.close_connection = True
            elif path.path in ('/api/result','/result-file'):
                args=urllib.parse.parse_qs(path.query)
                try:
                    document=app.store.result_document(args.get('id',[''])[0],args.get('file',[''])[0])
                    if path.path=='/result-file':
                        self.output(200,document.read_bytes(),'application/pdf' if document.suffix.lower()=='.pdf' else 'text/plain')
                    elif document.suffix.lower()=='.pdf':
                        self.output(200,{'name':document.name,'pdf':True})
                    else:
                        self.output(200,{'name':document.name,'text':document.read_text()})
                except (ValueError,OSError,UnicodeError):
                    self.output(404,{'error':'This result is not available'})
            else:
                self.output(404, {'error': 'Not found'})

        def browser_view(self, rest, short=False):
            """This computer's screen in noVNC (`browser_vnc`): the viewer's files, and its websocket to the VNC
            server. Only the owner, only from the dashboard's own page (a websocket ignores CORS, so another
            site could otherwise use the owner's tailnet identity). /browser and /browser/ are vnc.html itself,
            with noVNC's settings from this dashboard's defaults.json and mandatory.json."""
            if rest == 'region':  # where the browser's window is, for the viewer to open on it
                self.output(200, {'region': browser_viewer.window_region(app.config.get('browser_cdp_url') or browser_viewer.CDP_URL)})
                return
            if self.headers.get('Upgrade', '').lower() != 'websocket':
                web = app.config.get('browser_novnc') or browser_viewer.WEB
                found = browser_viewer.view_file(web, 'vnc.html' if short else rest)
                settings = rest in ('defaults.json', 'mandatory.json')  # also when this noVNC has none of its own
                if not found and not settings:
                    self.output(404, {'error': 'Not found'})
                    return
                data = found.read_bytes() if found else b'{}'
                base = dashboard_base(app.config, self.headers.get('Host', ''))
                if short:
                    data = browser_viewer.short_page(data.decode(), base).encode()
                elif settings:
                    try:
                        own = json.loads(data)
                    except ValueError:
                        own = {}
                    ours = browser_viewer.view_settings(base)[rest == 'mandatory.json']
                    data = json.dumps({**(own if isinstance(own, dict) else {}), **ours}).encode()
                self.send_response(200)
                self.send_header('Content-Type', browser_viewer.file_type(found or Path(rest)))
                self.send_header('Content-Length', str(len(data)))
                self.send_header('Cache-Control', 'no-cache')
                self.send_header('X-Content-Type-Options', 'nosniff')
                self.send_header('Referrer-Policy', 'no-referrer')
                self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; media-src 'self' data:; frame-ancestors 'self'")
                self.end_headers()
                try:
                    self.wfile.write(data)
                except (BrokenPipeError, ConnectionResetError):
                    self.close_connection = True
                return
            self.close_connection = True
            if (self.headers.get('Origin') != 'https://' + self.headers.get('Host', '') or self.headers.get('Sec-WebSocket-Version') != '13'
                    or not self.headers.get('Sec-WebSocket-Key')):
                self.output(403, {'error': 'The browser view opens from the dashboard'})
                return
            try:
                browser_viewer.bridge(self.rfile, self.connection, app.config['browser_vnc'], self.headers)
            except (OSError, ValueError) as error:
                print(f'browser view: {type(error).__name__}', file=sys.stderr, flush=True)
                try:
                    self.output(502, {'error': 'The screen is not reachable'})
                except OSError:
                    pass

        def consent(self):
            """The owner's Connect or Cancel on the consent page: a plain form, so its CSRF token is a field; the
            dashboard's own origin and the owner's sign-in, as for every owner change."""
            csrf = dashboard_csrf(app.token, app.config['tailscale_owner'])
            try:
                length = int(self.headers.get('Content-Length') or 0)
            except ValueError:
                length = 0
            # A page that was served under no-referrer (an older release's, still open) posts with `Origin: null`;
            # the browser's own Sec-Fetch-Site then says whether it came from this origin. The CSRF field stays required.
            origin = self.headers.get('Origin')
            same = (origin == 'https://' + self.headers.get('Host', '')
                    or origin in (None, 'null') and self.headers.get('Sec-Fetch-Site') == 'same-origin')
            if not self.owner():
                self.output(403, ai_access.refused_page('signin', lang=locale_prefs.language()), 'text/html')
                return
            if not same or not 0 < length <= 8192:
                self.output(403, ai_access.refused_page('expired', lang=locale_prefs.language()), 'text/html')
                return
            form = {k: v[0] for k, v in urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8', 'replace')).items()}
            if not hmac.compare_digest(str(form.get('csrf') or '').encode(), csrf.encode()):
                self.output(403, ai_access.refused_page('expired', lang=locale_prefs.language()), 'text/html')
                return
            try:
                where = app.ai_consent_post(form)
            except (ValueError, ai_access.OAuthError) as error:
                self.output(400, ai_access.error_page(str(error)), 'text/html')
                return
            self.send_response(303)
            self.send_header('Location', where)
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', '0')
            self.end_headers()

        def do_POST(self):
            route = urllib.parse.urlsplit(self.path).path
            if route in ai_access.PUBLIC_POST:
                self.ai('POST')
                return
            if route == ai_access.AUTHORIZE:
                self.consent()
                return
            if route == '/share-target':  # the installed app's Share before sw.js took over (it keeps shares itself): the dashboard, nothing read or kept
                self.close_connection = True
                self.send_response(303)
                self.send_header('Location', './')
                self.send_header('Cache-Control', 'no-store')
                self.send_header('Content-Length', '0')
                self.end_headers()
                return
            internal = self.internal()
            csrf = dashboard_csrf(app.token, app.config['tailscale_owner'])
            dashboard = (self.owner() and self.headers.get('Origin') == 'https://' + self.headers.get('Host', '') and
                         hmac.compare_digest(self.headers.get('X-CSRF-Token', '').encode(), csrf.encode()))
            if not internal and not dashboard:
                self.output(403, {'error': 'Unauthorized'})
                return
            if route == '/api/import-upload':  # Settings, Export: an export to import, streamed to disk (machine/app/export.py)
                return app.import_upload(self, bool(dashboard))
            request = None
            try:
                size = int(self.headers.get('Content-Length', '0'))
                upload = self.headers.get('X-Upload') in ('skill-import', 'graph-import', 'bug-report', 'meeting-notes')
                chat_file = self.headers.get('X-Upload') == 'chat-file'  # one file added to a chat message
                voice = self.headers.get('X-Upload') == 'voice'  # one recording for voice input (voice_input.py)
                if not 0 < size <= (UPLOAD_REQUEST_BYTES if upload else chat_files.REQUEST_BYTES if chat_file
                                    else voice_input.REQUEST_BYTES if voice else 65536):
                    if voice and size > 0:
                        self.close_connection = True
                        raise ValueError(f'Recordings can be up to {voice_input.MAX_SECONDS // 60} minutes.')
                    if chat_file and size > 0:
                        self.close_connection = True
                        raise ValueError(f'That file is too big. Files can be up to {chat_files.human(chat_files.FILE_BYTES)}.')
                    raise ValueError('Invalid request size')
                try:
                    request = json.loads(self.rfile.read(size))
                except OSError:
                    self.close_connection = True  # stalled or dropped client
                    return
                if ((upload and request.get('action') not in UPLOAD_ACTIONS) or (chat_file and request.get('action') != 'chat_upload')
                        or (voice and request.get('action') != 'voice_transcribe')):
                    raise ValueError('Invalid request size')
                if isinstance(request, dict) and re.fullmatch(r'[a-z0-9_]{1,60}', str(request.get('action'))):
                    self.action_name = request['action']  # the slow-request log names the action, never its arguments
                if self.path != '/api/action' or (not internal and request['action'] not in DASHBOARD_ACTIONS):
                    self.output(403, {'error': 'Operation is not available here'})
                    return
                owner_key = getattr(app, 'owner_token', '')
                if not dashboard and request['action'] in OWNER_ACTIONS and (
                        self.headers.get('X-Assistant-Client') == 'local-cli' or not owner_key or
                        not hmac.compare_digest(self.headers.get('X-Assistant-Owner', '').encode(), owner_key.encode())):
                    self.output(403, {'error': 'Owner decisions and feedback come from Telegram or the dashboard, not the local CLI'})
                    return
                if dashboard:
                    request.setdefault('args', {})['source'] = 'dashboard'
                result = app.action(request['action'], request.get('args', {}), owner_dashboard=bool(dashboard))
                # what a review, preparation or other agent reads names Slack members, never their ids
                self.output(200, result if dashboard else app.store.slack_named_out(result))
            except (ValueError, KeyError, TypeError, sqlite3.OperationalError, sqlite3.IntegrityError) as error:
                if not isinstance(error, ValueError):
                    # A request this action can't read (a page from before, a button that sent the wrong action) or a
                    # busy database: what to do about it, never "Invalid request"; the log says which action and why
                    LOG.warning('action failed action=%s error=%s', str(request.get('action') if isinstance(request, dict) else '')[:60],
                                type(error).__name__)
                if isinstance(error, KeyError) and not dashboard and error.args:  # an agent's call: the argument to add
                    self.output(400, {'error': f'Missing argument {str(error.args[0])[:60]}: add it and call again.'})
                    return
                self.output(400, {'error': str(error) if isinstance(error, ValueError) else ACTION_FAILED})
    return Handler
