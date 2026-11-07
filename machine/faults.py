"""The Machine's own errors (faults): where each was raised, its message with anything private taken out, whether it
is trouble outside this code, the log handler that keeps them (FaultLog, watch_faults) and the machine.fault signal
they become; the code version and release this Machine runs (code_version, running_release, source_url) and a
restart of the service (restart_self). Moved out of assistant.py as is, apart from APP_ROOT, which is the app folder
above machine/."""
import datetime as dt
import hashlib
import json
import logging
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import threading
import time
import traceback
import urllib.error
import urllib.parse

import error_feed
import locale_prefs
from machine.config import LOG
import next_actions
import service
from sources import SourceError
from timeutil import local_tz

# The Machine's own errors. A handler on the service log keeps, for each error raised in this
# code, its exception type, code location (file, line, function) and its message with anything
# private taken out (fault_message) per day: never arguments, values or content. The Gateway
# source turns them into machine.fault signals, so a review can offer to fix The Machine itself.
APP_ROOT = Path(__file__).resolve().parent.parent


FAULT_STEPS = (3, 10, 30, 100, 300, 1000)


# Trouble outside this code (a source, the network, the disk, a busy database) is not a bug to fix here.
EXTERNAL_ERRORS = (SourceError, OSError, subprocess.TimeoutExpired, sqlite3.OperationalError, KeyboardInterrupt, SystemExit)


def fault_frames(tb, root=APP_ROOT):
    frames = []
    for frame in traceback.extract_tb(tb):
        path = Path(frame.filename).resolve()
        if path.is_relative_to(root) and 'site-packages' not in path.parts:
            frames.append({'file': str(path.relative_to(root)), 'line': frame.lineno, 'function': frame.name})
    return frames[-8:]


def fault_where(error):
    """Where an error happened, for its log line: this code's frames, innermost first ("assistant.py:120 related_lines <
    assistant.py:88 run"), never values. '-' when none of it is ours."""
    return ' < '.join(f"{f['file']}:{f['line']} {f['function']}" for f in reversed(fault_frames(error.__traceback__)[-4:])) or '-'


FAULT_QUOTED = re.compile(r"'([^']*)'|\"([^\"]*)\"")


def fault_message(error, limit=200):
    """An error's own message, short and safe to keep: quoted text (except a lowercase key such as 'box'),
    email addresses, links, long numbers, ids and anything token-like are replaced. None when it has none."""
    text = ' '.join(str(error).split())
    text = re.sub(r'(?i)\bbearer\s+\S+', 'Bearer <secret>', text)
    text = re.sub(r'(?i)\b(token|secret|password|passwd|api[_-]?key|authorization|cookie)(["\']?\s*[:=]\s*)\S+', r'\1\2<secret>', text)
    text = re.sub(r'\b[a-z][a-z0-9+.-]*://\S+', '<link>', text, flags=re.I)
    text = re.sub(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+', '<email>', text)
    text = FAULT_QUOTED.sub(lambda m: m.group(0) if re.fullmatch(r'[a-z_][a-z0-9_.-]{0,40}', m.group(1) or m.group(2) or '') else '<text>', text)
    text = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '<id>', text, flags=re.I)
    # a plain code of lowercase words (android_feed_unavailable) stays: error_feed.PLAIN_CODE
    text = re.sub(r'(?<![\w<])[A-Za-z0-9_\-+/=]{24,}', lambda m: m.group(0) if error_feed.PLAIN_CODE.fullmatch(m.group(0)) else '<secret>', text)
    text = re.sub(r'\+?\d[\d .-]{4,}\d', '<number>', text)
    text = text.strip()
    return (text[:limit - 1] + '…' if len(text) > limit else text) or None


# What a fault means in plain words, by where it was logged (the first word of the log call): what
# failed and what the owner may notice.
FAULT_AREAS = {
    'fleet': ('Talking with your Fleet on The Machine Network', 'Teammates’ questions and answers may come late; your own to-dos are fine.'),
    'graph': ('Updating who knows whom', 'Who-knows-whom answers may be out of date.'),
    'enrichment': ('Looking up contact details', 'Some people may miss details such as their company.'),
    'embeddings': ('Indexing messages for search', 'Search may miss recent messages.'),
    'preparation': ('Preparing a to-do', 'A to-do may stay unprepared.'),
    'review': ('Checking new messages', 'New to-dos may come late.'),
    'sync': ('Reading a source', 'New messages from that source may come late.'),
    'collector': ('Reading a source', 'New messages from that source may come late.'),
    'delivery': ('Sending you to-dos', 'To-dos may reach you late.'),
    'promise': ('Tracking promises', 'Promise reminders may come late.'),
    'skill': ('Running a skill', 'A skill may not run.'),
    'skills': ('Running a skill', 'A skill may not run.'),
    'browser': ('The browser', 'Browser steps such as sign-ins may fail.'),
    'sign-in': ('Signing in', 'A sign-in may fail.'),
    'merge': ('Merging a fix', 'A fix may not be applied.'),
}


# Outside services by host, for naming the one that failed (the host itself is never kept).
OUTSIDE_SERVICES = (('themachine.computer', 'The Machine Network'), ('googleapis.com', 'Google'), ('google.com', 'Google'),
                    ('slack.com', 'Slack'), ('microsoft.com', 'Microsoft'), ('office.com', 'Microsoft'), ('salesflare.com', 'Salesflare'),
                    ('stripe.com', 'Stripe'), ('github.com', 'GitHub'), ('telegram.org', 'Telegram'), ('trello.com', 'Trello'),
                    ('shortcut.com', 'Shortcut'), ('x.com', 'X'), ('linkedin.com', 'LinkedIn'))


def outside_service(url):
    host = (urllib.parse.urlsplit(str(url or '')).hostname or '').lower()
    return next((name for suffix, name in OUTSIDE_SERVICES if host == suffix or host.endswith('.' + suffix)), 'An outside service')


def fault_origin(error):
    """The outside service an error came from, as {service, status}, or None when it is The Machine's own. Read from
    where it was raised, never its words: a typed error that says so (outside_service, like fleet.NetworkUnavailable),
    or an HTTP 5xx, timeout or dropped connection it was translated from (raise ... from it, or from None)."""
    seen = set()
    while error is not None and id(error) not in seen:
        seen.add(id(error))
        if getattr(type(error), 'outside_service', None):
            return {'service': type(error).outside_service, 'status': getattr(error, 'code', None)}
        if isinstance(error, urllib.error.HTTPError):
            return {'service': outside_service(error.url), 'status': error.code} if error.code >= 500 else None
        if isinstance(error, (TimeoutError, ConnectionError, urllib.error.URLError)):
            return {'service': outside_service(getattr(error, 'url', None)), 'status': None}
        # Follow only a deliberate translation: an error raised while handling another one is not caused by it.
        error = error.__cause__ or (error.__context__ if error.__suppress_context__ else None)
    return None


def fault_plain(location, count, config, origin=None):
    """One short paragraph: what failed, what the owner notices, and who acts."""
    words = str(location or '').lower().split()
    key = words[1] if words[:1] == ['thread'] and len(words) > 1 else (words[0] if words else '')
    what, notice = FAULT_AREAS.get(key, (f"Part of The Machine ({location})" if location else 'Part of The Machine',
                                         'Probably nothing yet: it tries again by itself.'))
    if origin:
        status = f" (it answered {origin['status']})" if origin.get('status') else ''
        return (f"{what} failed because {origin.get('service') or 'An outside service'} had a problem{status}, not The Machine. "
                f"{notice} The Machine tries again by itself; nothing is needed from you.")
    if count < 3:
        act = 'Nothing to do yet. If it keeps happening, The Machine offers a fix.'
    elif config.get('self_fix_auto', True) is False:
        act = 'The Machine can find the bug and test a fix in a copy; you review it and tap Merge.'
    else:
        act = 'The Machine can fix this itself: it tests a fix in a copy, and a small one merges by itself (undo for a day).'
    return f'{what} failed. {notice} {act}'


def code_version(root=APP_ROOT):
    try:
        result = subprocess.run(['git', '-C', str(root), 'rev-parse', '--short=12', 'HEAD'], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() or None


SOURCE_REPO = 'https://github.com/Salesflare/TheMachine'


RELEASE_TAG = re.compile(r'release-\d{8}-\d{4}')


_SOURCE_URL = {}


def source_url(root=APP_ROOT):
    """Where this Machine's code can be read (AGPL-3.0 section 13): the release tag it runs, else the latest release its
    code contains, else the release its last port names ("(OSS #12, release-…)"), else the repo. Never a local commit,
    which GitHub doesn't have."""
    ref = running_release(root)
    return f'{SOURCE_REPO}/tree/{ref}' if ref else SOURCE_REPO


def running_release(root=APP_ROOT):
    """The release this Machine's code is (or contains, or its last port names), or None: what source_url links and
    what the control plane compares with a fix's release before it tells the owner a bug they reported is fixed."""
    if 'url' in _SOURCE_URL and _SOURCE_URL['at'] > time.monotonic() - 600:
        return _SOURCE_URL['ref']
    git = lambda *args: subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True, timeout=10)
    ref = None
    try:
        for args in (('describe', '--tags', '--exact-match', '--match', 'release-*', 'HEAD'), ('describe', '--tags', '--abbrev=0', '--match', 'release-*', 'HEAD')):
            found = git(*args)
            if found.returncode == 0 and RELEASE_TAG.fullmatch(found.stdout.strip()):
                ref = found.stdout.strip()
                break
        if not ref:
            log = git('log', '-200', '--format=%s')
            ported = RELEASE_TAG.search(log.stdout) if log.returncode == 0 else None
            ref = ported and ported.group(0)
    except (OSError, subprocess.TimeoutExpired):
        pass
    _SOURCE_URL.update(at=time.monotonic(), url=True, ref=ref)
    return ref


class FaultLog(logging.Handler):
    def __init__(self, store, version=None, root=APP_ROOT):
        super().__init__(logging.ERROR)
        self.store, self.version, self.root = store, version, root

    def emit(self, record):
        # Called inside the except block that logged the error, so sys.exc_info() is that error.
        error = (record.exc_info or sys.exc_info())[1]
        # Where it happened in words, from the log call's own text without its values: "graph error=%s" -> "graph".
        self.record(error, re.sub(r'\s*\S*%[sdr]\S*', '', str(record.msg)).strip())

    def record(self, error, location):
        try:
            if error is None or isinstance(error, EXTERNAL_ERRORS):
                return
            frames = fault_frames(error.__traceback__, self.root)
            if not frames:
                return
            kind = type(error).__name__
            fingerprint = hashlib.sha256(json.dumps([kind] + [[f['file'], f['function']] for f in frames[-3:]]).encode()).hexdigest()[:16]
            self.store.record_fault(fingerprint, kind, frames, location[:120], self.version, fault_message(error), fault_origin(error))
            if hasattr(self.store, 'record_error'):  # and a signature for the error reports (error_feed.py)
                self.store.record_error('service', kind, str(error), frames[-1]['file'], frames[-1]['function'], frames[-1]['line'])
        except Exception:
            pass  # recording an error must never cause one


def watch_faults(store, root=APP_ROOT):
    """Record the service's own errors: logged ones and threads that die of one."""
    log = FaultLog(store, code_version(root), root)
    store.code_version = log.version
    LOG.addHandler(log)
    previous = threading.excepthook

    def hook(args):
        log.record(args.exc_value, 'thread ' + (args.thread.name if args.thread else ''))
        previous(args)
    threading.excepthook = hook
    return log


FAULT_WHERE = 'Where (innermost last):'  # the technical part of a fault signal starts here; the dashboard shows it under Details
# One line in each fault signal's metadata for the Do it run that fixes it: the product vision in short, so the fix is
# judged against it without the whole file in every prompt (vision: lean on tokens).
FIX_BY = ("Judge the fix against docs/vision.md: it's the owner's, and secure (their data, nothing unseen) first, then right, "
          'in their control, easy, calm, lean on tokens. Small, no reshuffles.')


def fault_event(account, row, config):
    frames = json.loads(row['frames'])
    top = frames[-1]
    count = row['count']
    message = row.get('message')
    origin = json.loads(row['origin']) if row.get('origin') else None
    lines = [fault_plain(row['location'], count, config, origin), '',
             f"Error: {row['kind']}" + (f': {message}' if message else ''),
             f"{(row['location'] or 'The service').capitalize()} failed {count} time{'s' if count > 1 else ''} on {row['day']} "
             f"(last {locale_prefs.clock_text(dt.datetime.fromisoformat(row['last_at']).astimezone(local_tz()))})."]
    lines += ['', FAULT_WHERE] + [f"  {f['file']}:{f['line']} in {f['function']}" for f in frames]
    if row.get('version'):
        lines += ['', 'Code version: ' + row['version']]
    return {'account_id': account['id'], 'source_id': f"fault:{row['fingerprint']}:{row['day']}", 'kind': 'machine.fault',
            'occurred_at': row['last_at'], 'title': f"The Machine: {row['kind']} in {top['function']}" + (f' ({count}×)' if count > 1 else ''),
            'body': '\n'.join(lines),
            'metadata': {'fault_kind': row['kind'], 'fingerprint': row['fingerprint'], 'location': row['location'], 'frames': frames,
                         'count': count, 'day': row['day'], 'version': row.get('version'), 'message': message,
                         'outside': origin,  # an outside service failed: nothing to fix in The Machine's code
                         'app_dir': str(next_actions.app_dir(config)), 'fix_dir': str(next_actions.fix_dir(config)), 'fix_by': FIX_BY, 'transport': 'internal',
                         'coverage': 'Errors raised in The Machine’s own code: type, code location and the message with anything private taken out, never values.'},
            'deleted': False}


DB_BUSY_RETRY = 15  # seconds: a sync that found the database busy (another writer's long transaction) reads again then


def db_busy(error):
    """Whether a sqlite3 error is only another writer holding the database (locked or busy past the busy timeout)."""
    return isinstance(error, sqlite3.OperationalError) and any(w in str(error).lower() for w in ('database is locked', 'database is busy', 'database table is locked'))


def restart_self(delay=5):
    """Restart this service a few seconds from now, from outside its own process, so the merge result
    is saved first. Only when it runs under systemd or launchd; returns whether a restart was scheduled."""
    if not service.running_as_service() or not service.available():
        return False
    unit = None
    if service.manager() == 'systemd':
        try:
            unit = next((part for part in Path('/proc/self/cgroup').read_text().strip().split('/')[::-1] if part.endswith('.service')), None)
        except OSError:
            unit = None
    return service.restart_later(unit or service.UNIT_NAME, delay)
