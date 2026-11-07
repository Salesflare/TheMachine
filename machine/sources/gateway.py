"""The OpenClaw Gateway's log as a source (Machine health): the journal lines it reads (GatewayJournal), how a line is
classified, one heartbeat event per half hour (gateway_event) and its sync (sync_gateway), which also brings the
service's own errors, the fixes an update set aside and the problems in the computer's own logs (machine/system_logs.py).
Moved out of assistant.py as is."""
import datetime as dt
import json
import re
import subprocess

from machine import system_logs
from machine.config import LOG
from machine.faults import code_version, fault_event
import next_actions
import parked_fixes
from sources import SourceError
from timeutil import local_tz, now


GATEWAY_SIGNALS = (
    # Owner-selected (October 10, 2026): agent runs that ended in an error on Telegram,
    # requests whose hand-off to another session was refused before dispatch, and
    # failed Telegram sends/edits/button answers. Restarts, model retries, memory
    # pressure and other routine Gateway noise are deliberately not collected.
    ('agent_run_failed', 'Agent run ended in an error', re.compile(r'\[telegram\] embedded run agent end: .*\bisError=true\b')),
    ('handoff_failed', 'Request hand-off failed before dispatch',
     re.compile(r'\[tools\] \S+ failed: .*(?:authority closed|authority is no longer active|before dispatch)', re.I)),
    ('telegram_send_failed', 'Telegram send failed',
     re.compile(r'\[telegram\] (?:\w+ failed[:!]|callback handler failed|spooled update \S+ failed)')),
)


GATEWAY_BUCKET = dt.timedelta(minutes=30)  # one review heartbeat


def gateway_classify(message):
    for kind, title, pattern in GATEWAY_SIGNALS:
        if pattern.search(message):
            return kind, title
    return None


def gateway_line(message):
    text = re.sub(r'^\d{4}-\d\d-\d\dT\S+\s+', '', message)
    text = re.sub(r'bot\d+:[A-Za-z0-9_-]{20,}', 'bot<redacted>', text)
    text = re.sub(r'(?i)\b(token|secret|password|api[_-]?key|authorization)(["\']?\s*[:=]\s*)\S+', r'\1\2<redacted>', text)
    text = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '<id>', text)
    return text[:1500]


class GatewayJournal:
    """Read-only journald reader for the OpenClaw Gateway unit."""
    def __init__(self, account):
        self.unit = account.get('unit', 'openclaw-gateway.service')

    def read(self, cursor=None, since=None):
        args = ['journalctl', '--user', '-u', self.unit, '-o', 'json', '--output-fields=MESSAGE', '--no-pager']
        args += ['--after-cursor', cursor] if cursor else ['--since', since]
        try:
            result = subprocess.run(args, capture_output=True, text=True, timeout=120)
        except (OSError, subprocess.TimeoutExpired) as error:
            raise SourceError('journal_unavailable:' + type(error).__name__) from None
        if result.returncode:
            raise SourceError('journal_read_failed')
        entries = []
        for line in result.stdout.splitlines():
            try:
                row = json.loads(line)
                message = row.get('MESSAGE') or ''
                if isinstance(message, list):  # journald encodes non-UTF-8 text as bytes
                    message = bytes(message).decode('utf-8', 'replace')
                at = dt.datetime.fromtimestamp(int(row['__REALTIME_TIMESTAMP']) / 1e6, dt.timezone.utc)
                entries.append((row['__CURSOR'], at, message))
            except (ValueError, KeyError, TypeError):
                raise SourceError('journal_invalid_entry') from None
        return entries


def gateway_event(account, source_id, bucket):
    local = lambda value: dt.datetime.fromisoformat(value).astimezone(local_tz()).strftime('%H:%M:%S')
    lines = [f"{local(line['at'])} {line['text']}" for line in bucket['lines']]
    more = bucket['count'] - len(bucket['lines'])
    if more > 0:
        lines.append(f'… and {more} more like this in the same half hour.')
    title = bucket['title'] + (f" ({bucket['count']}×)" if bucket['count'] > 1 else '')
    return {'account_id': account['id'], 'source_id': source_id, 'kind': 'gateway.alert',
            'occurred_at': bucket['lines'][0]['at'], 'title': title, 'body': '\n'.join(lines),
            'metadata': {'gateway_kind': bucket['kind'], 'count': bucket['count'], 'bucket_start': bucket['start'],
                         'bucket_minutes': int(GATEWAY_BUCKET.total_seconds() // 60), 'unit': account.get('unit', 'openclaw-gateway.service'),
                         'lines_shown': len(bucket['lines']), 'truncated': more > 0, 'transport': 'journald',
                         'coverage': 'Selected OpenClaw Gateway log lines grouped per kind and half hour; journal retention limits history.'},
            'deleted': False}


def sync_gateway(store, config, account, source=None, scan_logs=None):
    if source is None:  # the real journal: the computer's own logs too (a test passes its own source and scan)
        source, scan_logs = GatewayJournal(account), scan_logs or system_logs.scan
    state = store.checkpoint(account['id']) or {}
    last = state.get('last_at')
    since = f'@{int(dt.datetime.fromisoformat(last).timestamp())}' if last else f"-{int(account.get('bootstrap_hours', 24))}h"
    try:
        entries = source.read(state.get('cursor'), since)
    except SourceError:
        if not state.get('cursor'):
            raise
        # A rotated/vacuumed journal invalidates the cursor; resume from the last seen time.
        entries = source.read(None, since)
    buckets = state.get('open_buckets', {})
    changed = []
    for _, at, message in entries:
        found = gateway_classify(message)
        if not found:
            continue
        kind, title = found
        epoch = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
        start = (epoch + ((at - epoch) // GATEWAY_BUCKET) * GATEWAY_BUCKET).isoformat()
        source_id = f'{kind}:{start}'
        bucket = buckets.setdefault(source_id, {'kind': kind, 'title': title, 'start': start, 'count': 0, 'lines': []})
        bucket['count'] += 1
        if len(bucket['lines']) < 20:
            bucket['lines'].append({'at': at.isoformat(), 'text': gateway_line(message)})
        if source_id not in changed:
            changed.append(source_id)
    events = [gateway_event(account, source_id, buckets[source_id]) for source_id in changed]
    # The Machine's own errors come in through the first Gateway source.
    faults = []
    carries_faults = next((a['id'] for a in config.get('accounts', []) if a.get('service') == 'gateway'), None) == account['id']
    if carries_faults:
        faults = store.unreported_faults()
        events += [fault_event(account, row, config) for row in faults]
    # The computer's own logs (machine/system_logs.py): read at most every half hour, quietly, through the first Gateway
    # source as with the service's own errors; off with "computer_logs": false.
    found = []
    last_scan = state.get('computer_logs_at')
    if scan_logs and carries_faults and config.get('computer_logs', True) is not False and (
            not last_scan or dt.datetime.fromisoformat(now()) - dt.datetime.fromisoformat(last_scan) >= system_logs.EVERY):
        state['computer_logs_at'] = now()
        try:
            found = scan_logs()['findings']
        except Exception as error:  # a bug here never stops the Gateway's own log; it becomes a fault to fix
            LOG.error('computer logs error=%s', type(error).__name__, exc_info=True)
    # Only the last two windows can still grow; older ones are final.
    cutoff = (dt.datetime.fromisoformat(now()) - 2 * GATEWAY_BUCKET).isoformat()
    state.update(mode='incremental', cursor=entries[-1][0] if entries else state.get('cursor'),
                 last_at=entries[-1][1].isoformat() if entries else state.get('last_at'),
                 open_buckets={k: v for k, v in buckets.items() if v['start'] >= cutoff},
                 coverage='OpenClaw Gateway journal from the saved cursor; selected failure kinds only.')
    store.commit_page(account['id'], state, events)
    store.faults_reported(faults)
    if carries_faults:
        store.settle_faults(code_version(next_actions.app_dir(config)))
        # the Machine's own changes an update set aside come back as to-dos (parked_fixes.py)
        store.parked_fix_cards(account['id'], parked_fixes.pending(next_actions.app_dir(config)))
        if found:
            store.system_log_cards(account['id'], found)
    return {'mode': 'incremental', 'events': len(events)}
