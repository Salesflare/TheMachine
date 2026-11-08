"""The browser a task uses: its lease, recovering it when it is down, how long a step waits on it, the sign-in a task
waits for, the tabs a task has open, a task's own page with its steps, and the browser view's links. Moved out of
assistant.py as is."""
import contextlib
import datetime as dt
import json
import logging
from pathlib import Path
import re
import secrets
import sqlite3
import subprocess
import sys
import time
import urllib.parse

import browser_login
import browser_viewer
from machine.cards import HANDOFF
from machine.config import ROOT


def browser_lease_script(config=None):
    """The shared browser lease helper; `browser_lease_script` in config overrides the bundled one."""
    return Path((config or {}).get('browser_lease_script') or ROOT / 'integrations/browser-lease.py').expanduser()


def browser_read_failure(service, stderr):
    """Only fixed diagnostic codes, never the CLI's page text, URL or account details."""
    text = str(stderr).lower()
    if 'web client token not found' in text or 'not found in the web client' in text:
        return service + '_query_unavailable'
    if 'rejected the query' in text or 'query-failed' in text or 'http ' in text:
        status = re.search(r'http[ _:]*(\d{3})', text)
        return service + '_query_failed' + (':HTTP_' + status.group(1) if status else '')
    if any(sign in text for sign in BROWSER_DOWN):
        return service + '_browser_unreachable'
    if 'browser command failed' in text or 'target page, context or browser' in text:
        return service + '_browser_failed'
    return service + '_read_failed'


# The shared browser itself stopped answering (crashed, hung or closed), so no site in it can be read.
BROWSER_DOWN = ('connectovercdp', 'browser request timed out', 'econnrefused', 'browser is not running', 'browser not running',
                'browser has been closed', 'browser has disconnected')


BROWSER_RECOVERED = {}  # profile -> time.monotonic() of the last restart attempt


def recover_browser(profile, own_cdp=False, config=None):
    """Restart an unresponsive managed browser under an exclusive lease, at most once per 15 minutes.
    A busy lease waits for the next sync; external CDP/extension profiles and the Gateway stay untouched."""
    if own_cdp or profile in ('chrome', 'user') or time.monotonic() - BROWSER_RECOVERED.get(profile, -900) < 900:
        return False
    owner = 'browser-recovery-' + secrets.token_hex(8)
    lease = [sys.executable, str(browser_lease_script(config))]
    try:
        claimed = subprocess.run([*lease, 'claim', '--owner', owner, '--minutes', '5', '--exclusive'],
                                 capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return False
    if claimed.returncode:
        return False  # someone else is using it; don't consume the recovery cooldown
    BROWSER_RECOVERED[profile] = time.monotonic()
    try:
        def browser(*args):
            return subprocess.run(['openclaw', 'browser', '--browser-profile', profile, *args], capture_output=True, text=True, timeout=90)
        try:
            status = browser('--json', 'status')
            state = json.loads(status.stdout) if status.returncode == 0 else None
        except (OSError, subprocess.SubprocessError, ValueError):
            return False
        if not isinstance(state, dict):
            return False  # the Gateway did not answer: not this browser's to fix
        if state.get('running') and state.get('cdpReady') and state.get('cdpHttp'):
            return False
        try:
            if state.get('running'):
                browser('stop')
            started = browser('start').returncode == 0
        except (OSError, subprocess.SubprocessError):
            return False
        logging.warning('browser restart profile=%s ok=%s', profile, started)
        return started
    finally:
        try:
            subprocess.run([*lease, 'release', '--owner', owner], capture_output=True, text=True, timeout=15)
        except (OSError, subprocess.SubprocessError):
            pass  # the five-minute lease expires even if its helper is temporarily unavailable


AGENT_DB = Path.home() / '.openclaw/agents/main/agent/openclaw-agent.sqlite'


STEP_NAMES = {'exec': 'Running a command', 'browser': 'Using the browser', 'read': 'Reading a file', 'write': 'Writing notes',
              'edit': 'Writing notes', 'web_search': 'Searching the web', 'web_fetch': 'Reading a web page',
              'assistant_signals': 'Checking the assistant', 'memory_search': 'Searching memory'}


BROWSER_WAIT = 45  # seconds on the browser before a card offers it to the owner


SIGNIN_WATCH = 20  # seconds between looks at the browser while a task waits on the owner's sign-in


def browser_wait(db, job_id, status, at=None, reason=None):
    """The browser a preparation waits on, as {since, page, sign_in}: it has been on the browser for BROWSER_WAIT seconds or
    more (a sign-in, a captcha, a code or a page that does not load), or it stopped right after a browser step and
    asks for help. None otherwise. `page` is the last address it opened, when it said one.

    A blocker that hands a sign-in to the owner (`reason`, see HANDOFF) counts whenever the run used the browser at
    all: the handoff releases the browser lease (a command) after its last browser step, so the steps no longer end
    on the browser. Then `sign_in` is True."""
    if status not in ('starting', 'running', 'blocked'):
        return None
    try:
        calls = db.execute('SELECT tool,params,started_at FROM preparation_calls WHERE job_id=? ORDER BY started_at DESC,rowid DESC LIMIT 50',
                           (job_id,)).fetchall()
    except sqlite3.OperationalError:
        return None
    if status == 'blocked':  # saving the blocker is its own last step
        calls = [c for c in calls if c['tool'] != 'assistant_signals']
    streak = []
    for call in calls:
        if call['tool'] != 'browser':
            break
        streak.append(call)
    sign_in = status == 'blocked' and signin_handoff(reason)
    if not streak and sign_in:
        streak = [c for c in calls if c['tool'] == 'browser'][:1]
    if not streak:
        return None
    since = streak[-1]['started_at']
    if status != 'blocked' and (at or dt.datetime.now(dt.timezone.utc)) - dt.datetime.fromisoformat(since) < dt.timedelta(seconds=BROWSER_WAIT):
        return None
    return {'since': since, 'page': run_page(db, job_id, calls), 'sign_in': bool(sign_in)}


def run_page(db, job_id, calls):
    """The address of the tab a run left off in, from its own steps: the last address opened in the tab its last browser
    step used (OpenClaw's targetId, the tab's label), else the last one it opened. A run that only reused a tab an earlier
    run of the same task opened (a retry, or after a Change) looks in those runs, in that tab only. None when unknown:
    never another task's tab."""
    def params(call):
        try:
            found = json.loads(call['params']) if call['tool'] == 'browser' else {}
        except ValueError:
            return {}
        return found if isinstance(found, dict) else {}

    def address(call, tab):
        given = params(call)
        found = given.get('url') or given.get('targetUrl')
        if not isinstance(found, str) or urllib.parse.urlsplit(found).scheme not in ('http', 'https'):
            return None
        return found if tab is None or tab in (given.get('targetId'), given.get('label')) else None

    tab = next((params(c).get('targetId') or params(c).get('label') for c in calls if c['tool'] == 'browser'), None)
    tab = tab if isinstance(tab, str) and tab else None
    for call in calls:
        found = address(call, tab)
        if found:
            return found
    if tab is None:  # without its tab's name, an earlier run's address could be any tab
        return next((a for a in (address(c, None) for c in calls) if a), None)
    try:
        session = db.execute('SELECT session_job_id FROM preparation_runs WHERE job_id=?', (job_id,)).fetchone()
        earlier = db.execute('SELECT job_id FROM preparation_runs WHERE session_job_id=? AND job_id!=? ORDER BY started_at DESC LIMIT 10',
                             (session[0], job_id)).fetchall() if session else []
        for run in earlier:
            for call in db.execute("SELECT tool,params FROM preparation_calls WHERE job_id=? AND tool='browser' ORDER BY started_at DESC,rowid DESC LIMIT 200", (run[0],)):
                found = address(call, tab)
                if found:
                    return found
    except sqlite3.OperationalError:
        pass
    return None


def signin_handoff(reason):
    """A blocker that waits on the owner to sign in (a sign-in, a code, a passkey) rather than on something else."""
    return bool(reason) and bool(HANDOFF.search(reason)) and 'try again' not in reason.lower()


def signin_link(config, suggestion_id):
    """The dashboard address that opens the sign-in for a card blocked on one (Telegram's Sign in button), or None
    without a dashboard address."""
    host = str(config.get('dashboard_host') or '')
    return 'https://' + host + config.get('dashboard_path', '/') + '#signin-for=' + suggestion_id if host else None


SIGNIN_ADDRESS = re.compile(r'(?i)log-?in|sign-?in|/auth|oauth|\bsso\b|/idp|switch-account|account-?select|challenge|/2fa|/mfa|verif|captcha')


SIGNIN_KINDS = (('eid', re.compile(r'(?i)itsme|\be-?id\b|iamfas|\bcsam\b')), ('passkey', re.compile(r'(?i)passkey|security key')),
                ('captcha', re.compile(r'(?i)captcha|not a robot')),
                ('account', re.compile(r'(?i)switch-account|switch account|owning account|right account|choose (?:an |the )?account')),
                ('code', re.compile(r'(?i)authenticator|one-time|six-digit|\b2fa\b|two-factor|verification code|sms code')))


def signin_address(url, page):
    """A tab address that is still a sign-in for the task waiting on `page`: another site (its identity provider, such
    as itsme or eID) or a sign-in path on its own site."""
    parts = urllib.parse.urlsplit(str(url or ''))
    if parts.scheme not in ('http', 'https'):
        return False
    return not same_site(parts.hostname, page) or bool(SIGNIN_ADDRESS.search(parts.path + '?' + parts.query))


def signin_kind(reason, urls=()):
    """What a sign-in with nothing to type in the dialog wants (eid, passkey, captcha, account, code), from the task's
    blocker and its tab's address, or None. The blocker says it best; a code it offers next to another way ("an
    authenticator code or a security key") is a code, as that can go in the dialog."""
    for text in (reason or '', ' '.join(str(u) for u in urls)):
        kinds = [kind for kind, pattern in SIGNIN_KINDS if pattern.search(text)]
        if kinds:
            return 'code' if 'code' in kinds and 'passkey' in kinds else kinds[0]
    return None


def signin_name(reason, page):
    """The site's name as the task's blocker says it ("the open Drone Portal tab"), else its address."""
    found = re.search(r"\b(?:the|open)\s+(?:[a-z]+\s+)?([A-Z][\w.]*(?:\s+[A-Z][\w.]*){0,2})\s+(?:login\s+|sign-?in\s+)?tab\b", reason or '')
    return found.group(1) if found else browser_login.site(urllib.parse.urlsplit(page or '').hostname)


def same_site(a, b):
    """Two hosts of one site: equal, one under the other, or the same last two labels (login.wise.com, wise.com)."""
    a, b = (browser_login.site(urllib.parse.urlsplit(x).hostname if '//' in str(x or '') else x) for x in (a, b))
    if not a or not b:
        return False
    return a == b or a.endswith('.' + b) or b.endswith('.' + a) or a.split('.')[-2:] == b.split('.')[-2:]


TAB_LOOK = 5  # seconds: how often the cards read which tabs the Machine's browser has open (View in browser)


PEEK_EVERY = 2  # seconds: one look per task at most this often, however many dashboards watch


PEEK_WIDTH = 800  # pixels across: enough for a thumbnail and its larger view, small to send


def browser_result(call):
    """The JSON a browser step answered with (OpenClaw wraps it as text between markers), or {}."""
    try:
        content = json.loads(call['result'] or '{}').get('content') or []
        text = next(c['text'] for c in content if isinstance(c, dict) and isinstance(c.get('text'), str) and '---\n' in c['text'])
        found = json.loads(text.split('---\n', 1)[1].rsplit('\n<<<END', 1)[0])
    except (ValueError, TypeError, AttributeError, StopIteration, IndexError, KeyError):
        return {}
    return found if isinstance(found, dict) else {}


def peek_tab(db, job_id):
    """The tab a running preparation is on now, as (DevTools target ID, DevTools port), for the dashboard's live
    look at it: only while its latest step is a browser step, and only a tab this task opened itself (by the target
    ID its own `open` step answered with): this run's, or, when this run carries on in a tab an earlier run of the same
    task opened and left open (a retry, after a sign-in or a Change), that run's. None otherwise, never another task's
    tab or one the owner uses."""
    try:
        calls = db.execute('SELECT tool,params,result FROM preparation_calls WHERE job_id=? ORDER BY started_at DESC,rowid DESC LIMIT 200',
                           (job_id,)).fetchall()
    except sqlite3.OperationalError:
        return None
    if not calls or calls[0]['tool'] != 'browser':
        return None
    try:
        last = json.loads(calls[0]['params'] or '{}')
    except ValueError:
        return None
    if not isinstance(last, dict) or last.get('action') == 'close':
        return None
    return own_tab(db, job_id, calls, last.get('targetId') or last.get('label'))


def run_tab(db, job_id):
    """The tab a running preparation last worked in, as (DevTools target ID, port), also between its browser steps
    (peek_tab only while it is on one): the tab of its latest browser step, when this task opened it itself (own_tab).
    None otherwise."""
    try:
        calls = db.execute('SELECT tool,params,result FROM preparation_calls WHERE job_id=? ORDER BY started_at DESC,rowid DESC LIMIT 200',
                           (job_id,)).fetchall()
    except sqlite3.OperationalError:
        return None
    for call in calls:
        try:
            last = json.loads(call['params'] or '{}') if call['tool'] == 'browser' else None
        except ValueError:
            continue
        if isinstance(last, dict):
            return None if last.get('action') == 'close' else own_tab(db, job_id, calls, last.get('targetId') or last.get('label'))
    return None


def own_tab(db, job_id, calls, want):
    """(DevTools target ID, port) of the tab named `want` (a targetId or label a browser step used) that this run
    opened itself, or that an earlier run of the same task opened (a retry, after a sign-in or a Change), while it was
    not closed again. `calls` are this run's (tool, params, result), newest first. None otherwise."""
    def opened(calls, want=None):
        """A run's own tabs, newest first: (target ID, port, every name OpenClaw gave it). With `want`, only that tab
        and only while the run had not closed it again."""
        tabs = []
        for call in calls:
            try:
                given = json.loads(call['params'] or '{}')
            except ValueError:
                continue
            if call['tool'] != 'browser' or not isinstance(given, dict):
                continue
            if want and not tabs and given.get('action') == 'close' and str(want) in (str(given.get('targetId')), str(given.get('label'))):
                return []
            if given.get('action') != 'open':
                continue
            found = browser_result(call)
            target, ws = found.get('targetId'), urllib.parse.urlsplit(str(found.get('wsUrl') or ''))
            if not isinstance(target, str) or not re.fullmatch(r'[A-F0-9]{32}', target) or ws.hostname not in ('127.0.0.1', 'localhost', '::1') or not ws.port:
                continue
            names = {str(found.get(k)) for k in ('targetId', 'label', 'tabId', 'suggestedTargetId') if found.get(k)}
            if not want or str(want) in names:
                tabs.append((target, ws.port, names))
        return tabs

    mine = next(iter(opened(calls, want)), None)
    if not mine and want:  # carrying on in a tab an earlier run of this same task opened
        try:
            session = db.execute('SELECT session_job_id FROM preparation_runs WHERE job_id=?', (job_id,)).fetchone()
            earlier = db.execute('SELECT job_id FROM preparation_runs WHERE session_job_id=? AND job_id!=? ORDER BY started_at DESC LIMIT 10',
                                 (session[0], job_id)).fetchall() if session else []
        except sqlite3.OperationalError:
            earlier = []
        for run in earlier:
            found = opened(db.execute('SELECT tool,params,result FROM preparation_calls WHERE job_id=? ORDER BY started_at DESC,rowid DESC LIMIT 200',
                                      (run[0],)).fetchall(), want)
            if found:
                mine = found[0]
                break
    return (mine[0], mine[1]) if mine else None


def browser_link(config):
    """Where the owner sees the assistant's browser: `browser_url` (a hosted machine's viewer behind its sign-in, or
    the local noVNC viewer of browser_viewer.py), else with `browser_vnc` the dashboard's own live view of this
    computer's screen. None: the dashboard only brings the tab to the front; it does that with a link too."""
    url = str(config.get('browser_url') or '')
    if urllib.parse.urlsplit(url).scheme in ('http', 'https'):
        return url
    if config.get('browser_vnc') and config.get('dashboard_host'):
        return 'https://' + str(config['dashboard_host']) + browser_viewer.view_link(config.get('dashboard_path', '/'), config.get('browser_novnc') or browser_viewer.WEB)
    return None


FINAL_STEPS = ('submit', 'pay', 'book', 'sign', 'confirm', 'order', 'apply')  # outcome:'your_step': the click left to the owner


BROWSER_WORK = ('act', 'upload', 'dialog')  # browser steps that change a page (type, click, choose, upload, answer a dialog)


SECRET_PARAM = re.compile(r'(?i)^(?:.*(?:token|secret|passw(?:or)?d|pwd|session|sess|sid|auth|signature|credential|api_?key|jwt|otp|nonce|ticket|saml).*|key|sig|code|state|hash|x-amz-.*)$')


def safe_link(url):
    """An http(s) address that is fine to show or send: no user name or password, no query value whose name looks
    like a token, key, signature or session, and no fragment that carries one. None for anything else."""
    parts = urllib.parse.urlsplit(str(url or '').strip())
    if parts.scheme not in ('http', 'https') or not parts.hostname:
        return None
    query = urllib.parse.urlencode([(k, v) for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True) if not SECRET_PARAM.match(k)])
    fragment = '' if '=' in parts.fragment or re.search(r'(?i)token|secret|session', parts.fragment) else parts.fragment
    host = parts.hostname if not parts.port else f'{parts.hostname}:{parts.port}'
    host = f'[{host}]' if ':' in parts.hostname else host
    return urllib.parse.urlunsplit((parts.scheme, host, parts.path, query, fragment))


def task_page(db, suggestion_id):
    """The page a task's own browser work ended on, for its card's View in browser: {url, target, port, title, worked}
    from the newest run of this task that used the browser. `url` is the last address that run recorded for the tab
    its last browser step used (a step's answer says where the tab is now; else the address it opened), `target` that
    tab's DevTools ID when this task opened it and did not close it again (own_tab), `worked` whether a step there
    changed a page (typed, clicked, uploaded), not only read it. None without browser steps. Never another task's tab:
    only this task's runs and the tabs they named."""
    try:
        jobs = [r[0] for r in db.execute('SELECT job_id FROM preparation_runs WHERE suggestion_id=? ORDER BY started_at DESC LIMIT 20', (suggestion_id,))]
        current = db.execute('SELECT job_id FROM preparations WHERE suggestion_id=?', (suggestion_id,)).fetchone()
        if current and current[0] not in jobs:
            jobs.insert(0, current[0])
        used = {r[0] for r in db.execute("SELECT DISTINCT job_id FROM preparation_calls WHERE tool='browser' AND job_id IN (%s)" % ','.join('?' * len(jobs)), jobs)} if jobs else set()
        job = next((j for j in jobs if j in used), None)
        calls = db.execute('SELECT tool,params,result FROM preparation_calls WHERE job_id=? ORDER BY started_at DESC,rowid DESC LIMIT 200',
                           (job,)).fetchall() if job else []
    except sqlite3.OperationalError:
        return None
    def params(call):
        try:
            found = json.loads(call['params'] or '{}')
        except (ValueError, TypeError):
            return {}
        return found if isinstance(found, dict) else {}
    steps = [(params(c), c) for c in calls if c['tool'] == 'browser']
    if not steps:
        return None
    want = next((p.get('targetId') or p.get('label') for p, _ in steps if p.get('targetId') or p.get('label')), None)
    want = want if isinstance(want, str) and want else None
    closed = want and any(p.get('action') == 'close' and want in (str(p.get('targetId')), str(p.get('label'))) for p, _ in steps[:1])
    tab = None if closed else own_tab(db, job, calls, want)
    names = {want, tab[0] if tab else None} - {None}  # a step names its tab by label or ID; its answer by ID
    url = title = None
    for given, call in steps:
        if given.get('action') == 'tabs':
            continue  # a tab list names every tab, never this task's own
        answer = browser_result(call)
        found_names = {str(answer.get(k)) for k in ('targetId', 'label', 'tabId', 'suggestedTargetId') if answer.get(k)}
        for found, named in ((answer.get('url'), found_names), (given.get('url') or given.get('targetUrl'), {str(given.get('targetId')), str(given.get('label'))})):
            if isinstance(found, str) and urllib.parse.urlsplit(found).scheme in ('http', 'https') and (want is None or names & named):
                url, title = found, answer.get('title') if found == answer.get('url') else None
                break
        if url:
            break
    url = url or run_page(db, job, calls)
    if not url:
        return None
    return {'url': url, 'target': tab[0] if tab else None, 'port': tab[1] if tab else None,
            'title': ' '.join(str(title).split())[:80] if isinstance(title, str) and title.strip() else None,
            'worked': any(p.get('action') in BROWSER_WORK and (want is None or names & {str(p.get('targetId')), str(p.get('label'))}) for p, _ in steps)}


PANE_QUERY = 'autoconnect=1&reconnect=1&resize=remote&path=browser/websockify'  # noVNC's own settings, any release


def browser_view_link(config, suggestion_id):
    """The dashboard address that shows a task's page in the Machine's own browser (View in browser, also from
    Telegram): it brings that tab to the front, or reopens it there, then opens the browser's viewer. None without a
    dashboard address. It carries only the task's ID, never the page's address."""
    host = str(config.get('dashboard_host') or '')
    return 'https://' + host + config.get('dashboard_path', '/') + '#browser-for=' + suggestion_id if host else None


def transcript_tool_calls(session_key, agent_db=None, limit=4, scan=60):
    """[(at, tool name, arguments)] of the latest tool calls in an agent session, newest first, read from the
    agent's own transcript (read-only). Best effort: a missing or busy transcript gives none."""
    path = agent_db or AGENT_DB
    if not Path(path).exists():
        return []
    try:
        with contextlib.closing(sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=1)) as db:
            session = db.execute('SELECT session_id FROM session_windows WHERE session_key=? ORDER BY created_at DESC LIMIT 1',
                                 (session_key,)).fetchone()
            if not session:
                return []
            rows = db.execute('SELECT created_at,event_json,event_zstd FROM transcript_events WHERE session_id=? ORDER BY seq DESC LIMIT ?',
                              (session[0], scan)).fetchall()
    except sqlite3.Error:
        return []
    calls = []
    for created_at, text, packed in rows:
        if text is None and packed is not None:
            try:
                from compression import zstd
                text = zstd.decompress(packed).decode()
            except Exception:
                continue
        if not text or '"toolCall"' not in text:
            continue
        try:
            event = json.loads(text)
        except ValueError:
            continue
        message = event.get('message') if isinstance(event.get('message'), dict) else {}
        if message.get('role') != 'assistant' or not isinstance(message.get('content'), list):
            continue
        for part in reversed(message['content']):
            if isinstance(part, dict) and part.get('type') == 'toolCall':
                arguments = part.get('arguments') if isinstance(part.get('arguments'), dict) else {}
                calls.append((dt.datetime.fromtimestamp(created_at / 1000, dt.timezone.utc).isoformat(), part.get('name'), arguments))
        if len(calls) >= limit:
            break
    return calls[:limit]


def session_holds_since(session_key, since, agent_db=None):
    """True when the agent's current session for this key began before `since` (an ISO time) and was never compacted
    or reset: everything that happened in it since then is still in its context. Read-only; any doubt gives False."""
    path = agent_db or AGENT_DB
    try:
        start = int(dt.datetime.fromisoformat(since).timestamp() * 1000)
        if not Path(path).exists():
            return False
        with contextlib.closing(sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=1)) as db:
            session = db.execute('SELECT session_id,created_at FROM session_windows WHERE session_key=? ORDER BY created_at DESC LIMIT 1',
                                 (session_key,)).fetchone()
            return bool(session) and session[1] <= start and not db.execute(
                "SELECT 1 FROM transcript_event_identities WHERE session_id=? AND event_type IN ('compaction','reset') LIMIT 1",
                (session[0],)).fetchone()
    except (sqlite3.Error, ValueError, TypeError, OSError):
        return False


def preparation_steps(job_id, agent_db=None, limit=4):
    """The latest step titles of a running preparation, read from the agent's own transcript (read-only).

    Best effort: a missing or busy transcript simply shows no steps."""
    if not re.fullmatch(r'[a-f0-9]{32}', job_id or ''):
        return []
    steps = []
    for at, name, arguments in transcript_tool_calls('agent:main:assistant-review-preparation-' + job_id, agent_db, limit):
        title = arguments.get('title') if isinstance(arguments.get('title'), str) else ''
        steps.append({'title': ' '.join(title.split())[:120] or STEP_NAMES.get(name, 'Working'), 'at': at})
    return steps[::-1]
