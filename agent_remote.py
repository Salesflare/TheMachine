"""Hand to Claude Code / Hand to Codex where the CLI isn't the owner's own computer (agent_jobs.py, docs/agents.md).

- Claude (`remote`): the brief goes as a message to the owner's own Claude Code session, `claude -p <message> --cloud
  <session id>`. That session runs on their paired computer or in Anthropic's cloud, under their own Claude sign-in.
  It can't reach this Machine, so it hands the result back through The Machine's claude.ai connector: one tool,
  `report_result`, with a ticket made here for this job only. The Network keeps only the ticket's sha256 and the
  sealed result until this Machine fetches it (`/api/fleet/agent-results`).
- Codex (`cloud`): `codex cloud exec --env <id>`, followed with `codex cloud list --json` and, once it is ready,
  `codex cloud diff`. It runs in Codex cloud, under the owner's own ChatGPT sign-in.
- Codex on the owner's own computer (`device`): the hosted Machine registers a ticket's sha256 on the Network with the
  brief sealed end to end for that one computer (`dispatch`): network_crypto.seal, for the Network keys the computer
  published, signed with this Machine's own, bound to sender, computer and ticket. The Network relays the envelope and
  can't read it. The self-hosted Machine the owner paired on their computer asks for work with its own device token
  (serve: `jobs`), opens the brief with its private key (network-keys.json, never sent anywhere) after checking it was
  signed by its owner's hosted Machine, runs it there as an ordinary local job (a thread in the Codex app on that
  computer, under the Codex sign-in it has there), and reports progress and the result into that ticket (`progress`,
  `done`). The hosted Machine fetches it like a Claude result. Each side pins the other's keys the first time it sees
  them (agent_key_pins); when they change, nothing is sealed or opened until the computer is paired again.

None of them keeps, reads or moves a Claude or ChatGPT credential: the CLIs hold their own, on their own computer.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import logging
import re
import secrets
import subprocess
import threading
import time

import agent_jobs as aj
import network_crypto as nc

LOG = logging.getLogger('personal-assistant')
SESSION = re.compile(r'(?:session_|cse_)[A-Za-z0-9]{8,64}')
CODEX_TASK = re.compile(r'\btask_[a-z]_[0-9a-f]{16,64}\b')
REMOTE_DAYS = 2           # a remote Claude job waits this long for its result
POLL = 20                 # seconds between fetches while a remote job waits
CODEX_POLL = 15
SERVE_POLL = 30           # seconds between a paired computer's asks for Codex jobs
READY_TTL = 600           # seconds a paired computer trusts its `codex login status`
HASH = re.compile(r'[0-9a-f]{64}')
DONE = ('ready', 'applied')
FAILED = ('error', 'failed', 'cancelled')
PIN_SCHEMA = 'CREATE TABLE IF NOT EXISTS agent_key_pins(slot TEXT PRIMARY KEY,fingerprint TEXT NOT NULL,first_at TEXT NOT NULL)'
REPAIR = 'Its keys changed since it was paired. Pair it again on your Account page, then try again.'


def own_keys(jobs):
    """This Machine's Network keys (network-keys.json next to its database, made here once), or None."""
    import network
    path = network.keys_path(jobs.config)
    if not path:
        return None
    try:
        return nc.load_or_make(path)
    except (OSError, nc.SealError) as error:
        LOG.warning('agent keys error=%s', type(error).__name__)
        return None


def pinned(jobs, slot, public):
    """The other side's keys, checked (box key signed by its sign key) and pinned the first time: the keys, None when
    they don't check out, False when they differ from the pinned ones."""
    checked = nc.check_keys(public) if public else None
    if not checked:
        return None
    with jobs.connect() as db:
        db.execute(PIN_SCHEMA)
        row = db.execute('SELECT fingerprint FROM agent_key_pins WHERE slot=?', (slot,)).fetchone()
        if not row:
            db.execute('INSERT INTO agent_key_pins(slot,fingerprint,first_at) VALUES(?,?,?)', (slot, checked['fingerprint'], aj.now()))
            return public
    if row['fingerprint'] != checked['fingerprint']:
        LOG.warning('agent keys changed slot=%s', slot[:40])
        return False
    return public


def job_context(sender, device, digest):
    """What a sealed brief is bound to: from this hosted Machine, for that computer, for this ticket."""
    return {'p': 'codex-job', 'k': 'codex', 'f': sender, 't': device, 'r': digest}


def runner(row, command, own, jobs):
    if row['tool'] == 'claude':
        if not own.get('session'):
            raise aj.Stopped('missing', 'Pair a Claude Code session first')
        return RemoteClaude(command, own, jobs)
    if not own.get('env'):
        raise aj.Stopped('missing', 'Choose a Codex cloud environment first')
    return CloudCodex(command, own, jobs)


def session_id(value):
    """A Claude Code session id from what the owner pasted: the id itself or its claude.ai/code link."""
    found = SESSION.search(str(value or ''))
    return found.group(0) if found else None


def brief(prompt, ticket, mcp_url):
    return (f"{prompt.rstrip()}\n\n---\nThis job comes from The Machine. When you are done, call the `report_result` tool "
            f"of The Machine connector once, with ticket `{ticket}`, a short markdown summary, the finished text in `draft` "
            f"if the job asked for a message, and links such as a pull request. If that tool is not there, say so and "
            f"ask the owner to add the connector in claude.ai (Settings, Connectors, Add custom connector: {mcp_url}).")


def _run(argv, cwd, env, timeout=120):
    out = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL, env=env)
    said = re.sub(r'\x1b\[[0-9;?]*[A-Za-z]', '', (out.stdout or '') + '\n' + (out.stderr or ''))
    return out.returncode, said


def _last_line(said, fallback):
    lines = [x.strip() for x in said.splitlines() if x.strip()]
    return (lines[-1] if lines else fallback)[:300]


class RemoteClaude:
    def __init__(self, command, own, jobs):
        self.command, self.own, self.jobs = command, own, jobs
        self.config_dir = own.get('config_dir') if isinstance(own.get('config_dir'), str) else None

    def run(self, job, prompt, resume, folder, transcript, timeout, on_progress, on_session, procs):
        session = session_id(self.own.get('session'))
        if not session:
            raise aj.Stopped('missing', 'The paired Claude Code session id is not valid')
        ticket = secrets.token_urlsafe(24)
        digest = hashlib.sha256(ticket.encode()).hexdigest()
        try:
            made = self.jobs.network({'action': 'register', 'ticket_hash': digest, 'job': job['id']}) or {}
        except Exception as error:  # noqa: BLE001 - the Network's own message, never a secret
            raise aj.Stopped('failed', f'The Network could not take the job: {error}'[:300]) from None
        with self.jobs.connect() as db:
            db.execute('UPDATE agent_jobs SET token_hash=? WHERE id=?', (digest, job['id']))
        code, said = _run([self.command, '-p', brief(prompt, ticket, made.get('mcp_url') or 'https://app.themachine.computer/mcp'),
                           '--cloud', session], folder, aj.run_env(self.config_dir))
        with open(transcript, 'a', encoding='utf-8') as log:
            log.write(said[-20000:].replace(ticket, '<ticket>'))
        if code:
            raise aj.Stopped('failed', _last_line(said.replace(ticket, '<ticket>'), f'Claude Code stopped (exit {code})'))
        on_session(session)
        watch(self.jobs)
        return session, None  # the result comes back through the connector

    def link(self, session):
        return 'https://claude.ai/code/' + session if SESSION.fullmatch(str(session or '')) else 'https://claude.ai/code'

    def resume_watch(self, row):
        watch(self.jobs)


_watching = set()


def watch(jobs):
    """One thread per AgentJobs that fetches remote results while a remote job waits."""
    with jobs.lock:
        if id(jobs) in _watching:
            return
        _watching.add(id(jobs))
    threading.Thread(target=_poll, args=(jobs,), daemon=True, name='agent-results').start()


def _waiting(jobs):
    with jobs.connect() as db:
        return [dict(r) for r in db.execute("SELECT * FROM agent_jobs WHERE (place IN ('remote','device') AND status IN ('waiting','running') "
                                            "AND token_hash IS NOT NULL) OR token_hash IN (SELECT ticket_hash FROM agent_result_receipts WHERE acked=0)")]


def _poll(jobs):
    try:
        while True:
            rows = _waiting(jobs)
            if not rows:
                return
            fetch(jobs, rows)
            time.sleep(POLL)
    finally:
        with jobs.lock:
            _watching.discard(id(jobs))


def fetch(jobs, rows=None):
    rows = _waiting(jobs) if rows is None else rows
    if not rows:
        return 0
    by_hash = {r['token_hash']: r for r in rows}
    try:
        reply = jobs.network({'action': 'fetch', 'tickets': list(by_hash)}) or {}
    except Exception as error:  # noqa: BLE001 - try again on the next round
        LOG.warning('agent results fetch error=%s', type(error).__name__)
        reply = {}
    found, took = reply.get('results') or [], []
    for result in found:
        row = by_hash.get(result.get('ticket_hash'))
        if row and result.get('failed'):
            if stopped(jobs, row, result):
                took.append(row['token_hash'])
        elif row:
            if jobs.remote_result(row['id'], result):
                took.append(row['token_hash'])
    for going in reply.get('running') or []:  # a job on the owner's computer: which one, and how far it got
        row = by_hash.get(going.get('ticket_hash')) if isinstance(going, dict) else None
        if row and row['token_hash'] not in took:
            line = f"On {str(going.get('device') or 'your computer')[:60]}" + (f": {going['progress']}" if going.get('progress') else '')
            jobs.progress(row['id'], line[:200], turn=row['turns'])
    with jobs.connect() as db:
        receipts = [dict(r) for r in db.execute('SELECT ticket_hash,report FROM agent_result_receipts WHERE acked=0')]
    if receipts:
        try:
            reply = jobs.network({'action': 'ack', 'receipts': receipts}) or {}
        except Exception as error:  # noqa: BLE001 - durable receipts are retried after a restart too
            LOG.warning('agent results ack error=%s', type(error).__name__)
        else:
            with jobs.connect() as db:
                db.executemany('UPDATE agent_result_receipts SET acked=1 WHERE ticket_hash=? AND report=?',
                               [(r['ticket_hash'], r['report']) for r in reply.get('acked') or []
                                if r in receipts])
    cutoff = time.time() - REMOTE_DAYS * 86400
    for row in rows:
        started = row['started_at'] or row['created_at']
        if row['token_hash'] not in took and dt.datetime.fromisoformat(started).timestamp() < cutoff:
            jobs.finish(row['id'], 'failed', error=('No result came back. Open Codex on your computer to see where it got to.'
                                                    if row['place'] == 'device' else 'No result came back. Open it in Claude to see where it got to.'),
                        error_kind='timeout', only_if=('waiting', 'running'))
    return len(took)


def stopped(jobs, row, result):
    """The owner's computer said the job stopped there: the card says why, and the receipt is acknowledged once."""
    with jobs.connect() as db:
        previous = db.execute('SELECT report FROM agent_result_receipts WHERE ticket_hash=?', (row['token_hash'],)).fetchone()
    report_no = int(result.get('report') or 1)
    if previous and report_no <= previous['report']:
        return False
    kind = str(result.get('error_kind') or 'failed')[:40]
    error = str(result.get('summary') or 'It stopped on your computer.').strip()[:500]
    jobs.finish(row['id'], 'cancelled' if kind == 'cancelled' else 'failed', error=error, error_kind=kind,
                only_if=('waiting', 'running'), turn=row['turns'])
    with jobs.connect() as db:
        db.execute('INSERT INTO agent_result_receipts(ticket_hash,report,acked) VALUES(?,?,0) ON CONFLICT(ticket_hash) '
                   'DO UPDATE SET report=excluded.report,acked=0', (row['token_hash'], report_no))
    return True


def where(jobs):
    """Where the owner's Codex jobs go, from the Network: {'codex': 'machine'|'device'|'cloud'|None, 'devices': [...]},
    or None when it can't say now (the last answer stays)."""
    own = (aj.settings(jobs.config) or {}).get('codex')
    cloud = isinstance(own, dict) and own.get('place') == 'cloud' and bool(own.get('env'))
    try:
        found = jobs.network({'action': 'where', 'cloud_ready': cloud}) or {}
    except Exception as error:  # noqa: BLE001 - asked again later
        LOG.warning('agent where error=%s', type(error).__name__)
        return None
    devices = [{'label': str(d.get('label') or '')[:60], 'codex': bool(d.get('codex')), 'online': bool(d.get('online'))}
               for d in found.get('devices') or [] if isinstance(d, dict)][:10]
    return {'codex': found.get('codex') if found.get('codex') in ('machine', 'device', 'cloud') else None, 'devices': devices}


class DeviceCodex:
    """A hosted Machine's Codex job for the owner's own computer: handed over the Network, nothing runs here."""
    command = None

    def __init__(self, jobs):
        self.jobs = jobs

    def target(self):
        """The owner's computer to seal for (an online one that runs Codex first) and this Machine's key slot."""
        try:
            found = self.jobs.network({'action': 'where'}) or {}
        except Exception as error:  # noqa: BLE001 - the Network's own message, never a secret
            raise aj.Stopped('failed', f'The Network could not say where Codex runs: {error}'[:300]) from None
        ready = [d for d in found.get('devices') or [] if isinstance(d, dict) and d.get('codex') and d.get('id')]
        device = next((d for d in ready if d.get('online')), ready[0] if ready else None)
        if not device:
            raise aj.Stopped('missing', 'Set up Codex on your computer first')
        label = str(device.get('label') or 'your computer')[:60]
        if not device.get('keys'):
            raise aj.Stopped('missing', f'Update The Machine on {label}, then try again.')
        keys = pinned(self.jobs, 'to:' + str(device['id']), device['keys'])
        if keys is False:
            raise aj.Stopped('failed', f'{label}: {REPAIR}')
        if not keys or not found.get('me'):
            raise aj.Stopped('failed', f'The keys of {label} do not check out. Pair it again, then try again.')
        return device, keys, str(found['me'])

    def run(self, job, prompt, resume, folder, transcript, timeout, on_progress, on_session, procs):
        ticket = secrets.token_urlsafe(24)  # only its hash leaves this Machine: no one else can claim the result
        digest = hashlib.sha256(ticket.encode()).hexdigest()
        private = own_keys(self.jobs)
        if not private:
            raise aj.Stopped('failed', 'This Machine has no keys to seal the job with.')
        device, keys, me = self.target()
        try:
            sealed = nc.seal({'brief': prompt}, private, keys, job_context(me, device['id'], digest))
        except nc.SealError:
            raise aj.Stopped('failed', 'This job is too long to hand to your computer. Shorten it, then try again.') from None
        try:
            sent = self.jobs.network({'action': 'dispatch', 'tool': 'codex', 'job': job['id'], 'ticket_hash': digest, 'to': device['id'],
                                      'sealed': sealed, 'keys': nc.public_keys(private)}) or {}
        except Exception as error:  # noqa: BLE001 - the Network's own message, never a secret
            raise aj.Stopped('failed', f'The Network could not take the job: {error}'[:300]) from None
        with self.jobs.connect() as db:
            db.execute('UPDATE agent_jobs SET token_hash=? WHERE id=?', (digest, job['id']))
        if sent.get('device') and not sent.get('online'):
            on_progress(f"Waiting for {str(sent['device'])[:60]} to come online")
        watch(self.jobs)
        return None, None  # the result comes back from that computer through the Network

    def cancel(self, row):
        if row['token_hash']:
            try:
                self.jobs.network({'action': 'cancel', 'ticket_hash': row['token_hash']})
            except Exception as error:  # noqa: BLE001 - canceled here anyway
                LOG.warning('agent cancel error=%s', type(error).__name__)

    def link(self, session):
        return None

    def resume_watch(self, row):
        watch(self.jobs)


# ------------------------------------------------------------------ the owner's own computer: Codex jobs from their hosted Machine

RELAY_SCHEMA = """CREATE TABLE IF NOT EXISTS agent_relayed(ticket_hash TEXT PRIMARY KEY,job_id TEXT NOT NULL,
  reported INTEGER NOT NULL DEFAULT 0,progress TEXT,created_at TEXT NOT NULL)"""
_ready = {'at': None, 'ok': False}  # at: time.monotonic() of the last check, None for never (monotonic may start near 0 at boot)


def codex_ready(jobs, run=None):
    """Whether this computer can take Codex jobs: Codex is here and signed in (`codex login status`, which prints no
    secret; checked every READY_TTL). The sign-in stays Codex's own: nothing of it is read or sent."""
    own = (aj.settings(jobs.config) or {}).get('codex')
    if own is False or (isinstance(own, dict) and own.get('serve') is False):
        return False
    if _ready['at'] is not None and time.monotonic() - _ready['at'] < READY_TTL:
        return _ready['ok']
    command = aj.find('codex', own.get('command') if isinstance(own, dict) else None)
    ok = False
    if command:
        try:
            ok = (run or _run)([command, 'login', 'status'], None, aj.run_env(), 60)[0] == 0
        except (OSError, subprocess.SubprocessError):
            ok = False
    _ready.update(at=time.monotonic(), ok=ok)
    return ok


def serve(jobs, stop, run=None):
    """A paired self-hosted Machine: asks the Network for its owner's Codex jobs every SERVE_POLL seconds."""
    while not stop.is_set():
        try:
            serve_once(jobs, run)
        except Exception as error:  # noqa: BLE001 - asked again on the next round
            LOG.warning('agent serve error=%s', type(error).__name__)
        stop.wait(SERVE_POLL)


def serve_once(jobs, run=None):
    with jobs.connect() as db:
        db.execute(RELAY_SCHEMA)
    private = own_keys(jobs)
    ready = bool(private) and codex_ready(jobs, run)
    ask = {'action': 'jobs', 'tools': ['codex'] if ready else []}
    if private:
        ask['keys'] = nc.public_keys(private)  # published once; the Network seals nothing, the hosted Machine does
    reply = jobs.network(ask) or {}
    taken = 0
    for job in reply.get('jobs') or []:
        if ready and isinstance(job, dict):
            if take(jobs, job, private, str(reply.get('me') or '')):
                taken += 1
            digest = str(job.get('ticket_hash') or '')
            with jobs.connect() as db:
                saved = db.execute('SELECT 1 FROM agent_relayed WHERE ticket_hash=?', (digest,)).fetchone()
            if saved:
                # The brief and ticket are committed locally before the relay can discard them. A lost ack is
                # retried on redelivery; take()'s unique ticket prevents a second launch.
                jobs.network({'action': 'received', 'ticket_hash': digest})
    for digest in reply.get('cancelled') or []:
        with jobs.connect() as db:
            row = db.execute('SELECT job_id FROM agent_relayed WHERE ticket_hash=?', (str(digest),)).fetchone()
        if row:
            try:
                jobs.cancel(row['job_id'])
            except ValueError:
                pass  # it ended meanwhile
    report(jobs)
    return taken


def opened(jobs, job, private, me):
    """The brief of a job sealed for this computer, or (None, why): it must be sealed for this computer's own key, for
    this ticket, and signed by the hosted Machine whose keys this computer pinned (pairing again starts over)."""
    digest, sender = str(job.get('ticket_hash') or ''), str(job.get('from') or '')
    if not (me and sender.startswith('m:')):
        return None, 'It came without who sent it, so it was not opened.'
    keys = pinned(jobs, 'from:' + me + ':' + sender, job.get('from_keys'))
    if keys is False:
        return None, 'The keys of your Machine changed since this computer first saw them. Pair this computer again.'
    if not keys:
        return None, 'It was not signed by your Machine, so it was not opened.'
    try:
        body = nc.open_sealed(job.get('sealed'), private, keys, job_context(sender, me, digest))
    except nc.SealError:
        return None, 'It did not open on this computer, so it was not run.'
    brief = body.get('brief') if isinstance(body, dict) else None
    if not isinstance(brief, str) or not brief.strip() or len(brief) > 60_000:
        return None, 'It came without a job to run.'
    return brief, None


def take(jobs, job, private=None, me=''):
    """One job from the owner's hosted Machine: an ordinary local Codex job here, in a folder of its own. A brief that
    doesn't open (or isn't signed by the owner's Machine) is never run: that side hears why."""
    digest = str(job.get('ticket_hash') or '')
    if job.get('tool') != 'codex' or not HASH.fullmatch(digest):
        return False
    brief, why = opened(jobs, job, private, me) if private else (None, 'This computer has no keys to open it.')
    if why:
        LOG.warning('agent job not opened ticket=%s', digest[:12])
        try:
            jobs.network({'action': 'done', 'ticket_hash': digest, 'failed': True, 'error_kind': 'sealed', 'summary': why})
        except Exception as error:  # noqa: BLE001 - that side times out instead
            LOG.warning('agent report error=%s', type(error).__name__)
        return False
    job_id, at = 'aj_' + secrets.token_hex(8), aj.now()
    with jobs.connect() as db:
        db.execute('BEGIN IMMEDIATE')
        if db.execute('SELECT 1 FROM agent_relayed WHERE ticket_hash=?', (digest,)).fetchone():
            return False
        db.execute('INSERT INTO agent_jobs(id,suggestion_id,tool,place,status,brief,asks,turns,token_hash,created_at,updated_at) '
                   'VALUES(?,?,?,?,?,?,?,?,?,?,?)', (job_id, aj.RELAYED + digest[:16], 'codex', 'local', 'sent', brief, '[]', 1, digest, at, at))
        db.execute('INSERT INTO agent_relayed(ticket_hash,job_id,created_at) VALUES(?,?,?)', (digest, job_id, at))
    try:
        jobs.prepare_folder(job_id, brief, {})
    except OSError as error:
        jobs.finish(job_id, 'failed', error='I could not make the job folder on this computer', error_kind='folder')
        LOG.error('agent job folder error=%s', type(error).__name__)
        return True
    jobs.launch(job_id, brief, resume=None)
    return True


def report(jobs):
    """Tells the Network how each job from the hosted Machine is doing: its progress line while it runs, then its
    result (summary, changes, a rewritten message) or why it stopped, once."""
    with jobs.connect() as db:
        rows = [dict(r) for r in db.execute('SELECT r.ticket_hash, r.progress AS sent, j.* FROM agent_relayed r '
                                            'JOIN agent_jobs j ON j.id=r.job_id WHERE r.reported=0')]
    for row in rows:
        try:
            if row['status'] in ('result', 'failed', 'cancelled'):
                jobs.network(done_body(jobs, row))
                with jobs.connect() as db:
                    db.execute('UPDATE agent_relayed SET reported=1 WHERE ticket_hash=?', (row['ticket_hash'],))
            elif row['status'] == 'running' and (row['progress'] or 'Running') != row['sent']:
                line = row['progress'] or 'Running'
                jobs.network({'action': 'progress', 'ticket_hash': row['ticket_hash'], 'progress': line[:200]})
                with jobs.connect() as db:
                    db.execute('UPDATE agent_relayed SET progress=? WHERE ticket_hash=?', (line, row['ticket_hash']))
        except Exception as error:  # noqa: BLE001 - told on the next round; a ticket the Network forgot is not retried
            if 'not a job this computer took' in str(error):
                with jobs.connect() as db:
                    db.execute('UPDATE agent_relayed SET reported=1 WHERE ticket_hash=?', (row['ticket_hash'],))
            LOG.warning('agent report error=%s', type(error).__name__)


def done_body(jobs, row):
    body = {'action': 'done', 'ticket_hash': row['ticket_hash']}
    if row['status'] != 'result':
        return {**body, 'failed': True, 'error_kind': row['error_kind'] or row['status'],
                'summary': (row['error'] or 'It stopped on this computer.')[:500]}
    draft = ''
    found = jobs.work(row['id']) / aj.DRAFT_FILE
    if aj.DRAFT_FILE in [f.get('path') for f in json.loads(row['files'] or '[]')]:
        try:
            if not found.is_symlink() and found.stat().st_size <= 50_000:
                draft = found.read_text(errors='replace').strip()
        except OSError:
            draft = ''
    links = [u for u in dict.fromkeys(aj.URL.findall(row['summary'] or '')) if u.startswith('https://')][:10]
    return {**body, 'summary': (row['summary'] or 'Done, without a summary.')[:aj.SUMMARY_MAX],
            'diff': (row['diff'] or '')[:aj.DIFF_MAX], 'draft': draft, 'links': links}


class CloudCodex:
    def __init__(self, command, own, jobs):
        self.command, self.own, self.jobs = command, own, jobs
        self.env = str(own.get('env'))

    def run(self, job, prompt, resume, folder, transcript, timeout, on_progress, on_session, procs):
        branch = self.own.get('branch')
        argv = [self.command, 'cloud', 'exec', '--env', self.env, *(['--branch', str(branch)] if branch else []), prompt]
        code, said = _run(argv, folder, aj.run_env())
        with open(transcript, 'a', encoding='utf-8') as log:
            log.write(said[-20000:])
        task = CODEX_TASK.search(said)
        if code or not task:
            raise aj.Stopped('failed', _last_line(said, f'Codex cloud stopped (exit {code})'))
        on_session(task.group(0))
        return self.follow(job, task.group(0), time.time(), timeout, on_progress, procs)

    def task(self, task_id):
        code, said = _run([self.command, 'cloud', 'list', '--json', '--env', self.env, '--limit', '20'], None, aj.run_env(), 60)
        try:
            tasks = json.loads(said.strip().splitlines()[0] if said.strip() else '{}').get('tasks') or []
        except (ValueError, AttributeError, IndexError):
            tasks = []
        return next((t for t in tasks if isinstance(t, dict) and t.get('id') == task_id), None)

    def follow(self, job, task_id, started, timeout, on_progress, procs):
        handle = aj.Handle(lambda: None)
        procs[job['id']] = handle
        last = None
        try:
            while True:
                if handle.cancelled:
                    raise aj.Stopped('cancelled', 'Canceled here. It may still finish in Codex cloud.')
                if time.time() - started > max(timeout, 3600):
                    raise aj.Stopped('timeout', 'Still running in Codex cloud. Open it there.')
                found = self.task(task_id) or {}
                status = str(found.get('status') or '').lower()
                if status and status != last:
                    on_progress({'pending': 'Running in Codex cloud'}.get(status, 'Codex cloud: ' + status)[:160])
                    last = status
                if status in FAILED:
                    raise aj.Stopped('failed', 'Codex cloud stopped. Open it there to see why.')
                if status in DONE:
                    code, diff = _run([self.command, 'cloud', 'diff', task_id], None, aj.run_env(), 120)
                    diff = diff.strip() + '\n' if not code and diff.strip() else ''
                    files = sorted(set(re.findall(r'^\+\+\+ b/(.+)$', diff, re.M)))[:aj.FILES_MAX]
                    title = str(found.get('title') or 'Done in Codex cloud').strip()
                    summary = f"{title}\n\n{len(files)} file{'s' if len(files) != 1 else ''} changed. Open it in Codex cloud to make a pull request."
                    self.jobs.result(job['id'], task_id, summary[:aj.SUMMARY_MAX], files=[{'path': f, 'size': 0} for f in files],
                                     diff=diff[:aj.DIFF_MAX])
                    return task_id, None  # the result is in already
                time.sleep(CODEX_POLL)
        finally:
            procs.pop(job['id'], None)

    def link(self, task_id):
        return 'https://chatgpt.com/codex/tasks/' + task_id if CODEX_TASK.fullmatch(str(task_id or '')) else 'https://chatgpt.com/codex'

    def resume_watch(self, row):
        if row['session_id'] and CODEX_TASK.fullmatch(row['session_id']):
            def go():
                try:
                    since = dt.datetime.fromisoformat(row['started_at']).timestamp() if row['started_at'] else time.time()
                    self.follow(row, row['session_id'], since, self.jobs.timeout, lambda line: self.jobs.progress(row['id'], line), self.jobs.procs)
                except aj.Stopped as stop:
                    self.jobs.finish(row['id'], 'cancelled' if stop.kind == 'cancelled' else 'failed', error=str(stop)[:500], error_kind=stop.kind)
            threading.Thread(target=go, daemon=True, name='agent-job').start()
