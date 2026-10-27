"""Report a bug, when it can't go out now: the report stays on this Machine and goes by itself later.

A report the owner sent goes to the control plane (fleet.Fleet.bug_report). When that can't take it now (it said 429,
with when to come back; it is away, 5xx; or this Machine is offline), the report is kept here, next to the database
(bug-queue.json, only this Machine's user reads it), and the service sends it when it is due (assistant's
bug_queue_worker): at the control plane's Retry-After, else after a wait that doubles from a minute up to an hour. The
dashboard says when it goes out ("Saved. It goes out by itself at 10:55.") and shows the reports still waiting. Only
a refusal that retrying can't fix (the report itself was refused, or this Machine isn't linked) is an error."""
from __future__ import annotations

import json
import logging
import os
import secrets
import threading
import time
from pathlib import Path

import fleet

LOG = logging.getLogger('assistant.bug_queue')
MOST = 10  # reports kept waiting at once; one more is an error that says to email support
FIRST, LONGEST = 60, 3600  # seconds: the first wait without a Retry-After, and the longest
_LOCK = threading.Lock()


class Full(ValueError):
    """Too many reports are waiting already."""


def retryable(error):
    """Whether sending again later can work: a limit, the Network or control plane away, no connection."""
    return isinstance(error, (fleet.Limited, fleet.NetworkUnavailable, fleet.Off, OSError))


def wait(tries, retry_after=0):
    return max(int(retry_after or 0), min(LONGEST, FIRST * 2 ** max(tries, 0)))


def path(config):
    return Path(config['database']).expanduser().parent / 'bug-queue.json'


def load(config):
    try:
        found = json.loads(path(config).read_text())
    except (OSError, ValueError):
        return []
    return [i for i in found if isinstance(i, dict) and isinstance(i.get('body'), dict)] if isinstance(found, list) else []


def _save(config, items):
    file = path(config)
    temp = file.with_name(file.name + '.tmp')
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as out:
        json.dump(items, out)
    os.replace(temp, file)


def add(config, body, retry_after=0, clock=None):
    """Keeps the report to send later. Returns it ({'id', 'next_at', ...}); Full when too many wait already."""
    clock = clock or time.time
    with _LOCK:
        items = load(config)
        if len(items) >= MOST:
            raise Full('Too many reports are waiting to go out. Email support@themachine.computer.')
        item = {'id': 'bq_' + secrets.token_hex(6), 'body': body, 'tries': 0, 'queued_at': int(clock()),
                'next_at': int(clock()) + wait(0, retry_after)}
        _save(config, items + [item])
    LOG.info('bug report kept to send later wait=%d', item['next_at'] - item['queued_at'])
    return item


def view(config):
    """The reports still waiting, for Report a bug: the first words and when each goes out."""
    return [{'id': i['id'], 'what': str(i['body'].get('description') or '')[:80], 'next_at': i['next_at']} for i in load(config)]


def flush(config, send, clock=None):
    """Sends the reports that are due, oldest first, one at a time (nothing is locked while one goes). One the control
    plane can't take yet waits again, and so do the others, at least as long; one it refuses for good is logged and
    dropped. Returns how many went."""
    clock, sent = clock or time.time, 0
    while True:
        with _LOCK:
            item = next((i for i in load(config) if i['next_at'] <= clock()), None)
        if not item:
            return sent
        try:
            send(item['body'])
            error = None
        except Exception as failed:  # noqa: BLE001 - one report's trouble never stops the service
            error = failed
        with _LOCK:
            items = load(config)
            if error is not None and retryable(error):  # it keeps its place; the others wait at least as long
                hold = int(clock()) + wait(item['tries'] + 1, getattr(error, 'retry_after', 0))
                for other in items:
                    if other['id'] == item['id']:
                        other['tries'] = item['tries'] = item['tries'] + 1
                    other['next_at'] = max(other['next_at'], hold)
            else:
                items = [i for i in items if i['id'] != item['id']]
            _save(config, items)
        if error is None:
            sent += 1
            LOG.info('bug report sent after waiting tries=%d', item['tries'])
        elif retryable(error):
            LOG.info('bug report still waiting tries=%d error=%s', item['tries'], type(error).__name__)
            return sent
        else:
            LOG.warning('bug report refused for good, dropped error=%s', type(error).__name__)
