"""How much of the owner's model plan is used and when it resets (model_usage, model_status, Codex's app server for
ChatGPT's limits), and how node scripts run here (node_bin, node_env, the Telegram account they use). Moved out of
assistant.py as is."""
import contextlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import threading
import time

from models import claude_plan_route, openclaw_model
import portable
from timeutil import now
from machine.owner_error import OwnerError


def usage_status(config, run=subprocess.run):
    """The running OpenClaw Gateway's own usage reading (`usage.status`): a short RPC client, not a second Gateway,
    and no model call. The raw reply, or None."""
    try:
        result = run([str(config.get('openclaw') or 'openclaw'), 'gateway', 'call', 'usage.status', '--json',
                      '--timeout', '60000', '--params', '{}'], capture_output=True, text=True, timeout=90)
        data = json.loads(result.stdout)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    return data if isinstance(data, dict) else None


def model_usage(config, run=subprocess.run, reply=None):
    """How much of its limits the AI sign-in reports used (ChatGPT: the 5-hour and weekly windows), as the running
    OpenClaw Gateway reads it (`usage.status`): a short RPC client, not a second Gateway. Only names, labels,
    percentages and reset times are kept; None when nothing is known."""
    data = usage_status(config, run) if reply is None else reply
    found = []
    for entry in (data.get('providers') or []) if isinstance(data, dict) else []:
        if not isinstance(entry, dict) or not isinstance(entry.get('provider'), str):
            continue
        windows = [{'label': str(w.get('label') or '')[:20], 'used': max(0, min(100, round(float(w['usedPercent'])))),
                    'reset': int(w['resetAt']) // 1000 if isinstance(w.get('resetAt'), (int, float)) else None}
                   for w in entry.get('windows') or [] if isinstance(w, dict) and isinstance(w.get('usedPercent'), (int, float))]
        if windows:
            found.append({'provider': entry['provider'][:40], 'name': str(entry.get('displayName') or entry['provider'])[:40],
                          'windows': windows[:4]})
    return found or None


# Where ChatGPT shows the Codex usage limits and the usage limit resets: the way to see or use one by hand.
CHATGPT_USAGE_PAGE = 'https://chatgpt.com/codex/cloud/settings/usage'


class CodexAppServer:
    """The Codex CLI's own app-server (its supported JSON-RPC interface) with the Codex CLI's own ChatGPT sign-in:
    it can read the usage limit resets and use one, which OpenClaw does not offer. No model call; nothing here sees a
    token. Used only when that sign-in is the same ChatGPT account OpenClaw uses. A hard deadline stops it."""

    def __init__(self, config, timeout=20, popen=subprocess.Popen):
        binary = config.get('codex', shutil.which('codex'))
        self.proc = None
        if not binary:
            return
        try:
            self.proc = popen([str(binary), 'app-server'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True, **portable.new_group())
        except OSError:
            return
        self.timer = threading.Timer(timeout, self.close)
        self.timer.daemon = True
        self.timer.start()
        self.next_id = 0
        if self.call('initialize', {'clientInfo': {'name': 'the_machine', 'title': 'The Machine', 'version': '1'}}) is None:
            self.close()
        else:
            self.send({'method': 'initialized'})

    def send(self, message):
        self.proc.stdin.write(json.dumps(message) + '\n')
        self.proc.stdin.flush()

    def call(self, method, params=None):
        """One request's result, or None (no app-server, an error, or the deadline)."""
        if not self.proc:
            return None
        self.next_id += 1
        try:
            self.send({'id': self.next_id, 'method': method, **({} if params is None else {'params': params})})
            for line in self.proc.stdout:
                try:
                    message = json.loads(line)
                except ValueError:
                    continue
                if isinstance(message, dict) and message.get('id') == self.next_id:
                    return message.get('result') if isinstance(message.get('result'), dict) else None
        except (OSError, ValueError, AttributeError):
            pass
        return None

    def close(self):
        proc, self.proc = self.proc, None
        if proc:
            with contextlib.suppress(OSError):
                proc.stdin.close()
            portable.end_group(proc)  # its whole group: a child must not hold the pipe open
            with contextlib.suppress(OSError, ValueError):
                proc.stdout.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
        if getattr(self, 'timer', None):
            self.timer.cancel()


def codex_same_account(server, reply):
    """Is the Codex CLI signed in to the ChatGPT account OpenClaw uses? Same email and, when both say, same plan."""
    account = (server.call('account/read', {'refreshToken': False}) or {}).get('account') or {}
    entry = next((p for p in (reply or {}).get('providers') or [] if isinstance(p, dict) and p.get('provider') == 'openai'), {})
    email, theirs = str(entry.get('accountEmail') or '').strip().lower(), str(account.get('email') or '').strip().lower()
    plans = entry.get('plan'), account.get('planType')
    return (account.get('type') == 'chatgpt' and bool(email) and email == theirs
            and (not all(plans) or plans[0] == plans[1]))


def model_resets(config, reply, server_factory=None):
    """The ChatGPT usage limit resets available to the account OpenClaw uses, through the Codex CLI's own sign-in when
    it is the same account; None when that cannot be known (no Codex CLI, another account, an older Codex)."""
    with (server_factory or CodexAppServer)(config) as server:
        if not codex_same_account(server, reply):
            return None
        limits = server.call('account/rateLimits/read')
    resets = (limits or {}).get('rateLimitResetCredits')
    if not isinstance(resets, dict) or not isinstance(resets.get('availableCount'), int):
        return None
    credits = [{'title': str(c.get('title') or '')[:80] or None,
                'expires': int(c['expiresAt']) if isinstance(c.get('expiresAt'), (int, float)) else None}
               for c in resets.get('credits') or [] if isinstance(c, dict) and c.get('status') in (None, 'available')]
    return {'available': max(0, resets['availableCount']), 'credits': credits[:10],
            'allowed': limits.get('ordinaryUsageAllowed') if isinstance(limits.get('ordinaryUsageAllowed'), bool) else None}


def model_status(config, reply, usage, resets, checked_at=None):
    """What Settings shows about the model: which one, through which sign-in and plan, how much of each limit is
    used, whether a limit is reached and when it lifts, and the resets. No email, no account ids, no tokens."""
    entry = next((p for p in (reply or {}).get('providers') or [] if isinstance(p, dict) and p.get('provider') == 'openai'), None)
    model = openclaw_model(config)
    windows = [w for p in usage or [] for w in p['windows']]
    now_s = time.time()
    full = [w for w in windows if w['used'] >= 100 and (w['reset'] or now_s + 1) > now_s]
    reached = bool(full) or (resets or {}).get('allowed') is False
    return {'model': model, 'provider': (model or '').split('/')[0] or (entry or {}).get('provider'),
            'chatgpt': bool(entry and entry.get('accountEmail')), 'claude_plan': claude_plan_route(config),
            'plan': re.sub(r'^self_serve_', '', str((entry or {}).get('plan') or ''))[:40].replace('_', ' ') or None,
            'windows': windows, 'limit_reached': reached,
            'limit_resets_at': max((w['reset'] for w in full if w['reset']), default=None) if reached else None,
            'resets': resets, 'can_reset': bool(resets and resets['available'] > 0),
            'usage_page': CHATGPT_USAGE_PAGE if entry else None, 'checked_at': checked_at or now()}


def use_model_reset(config, reply, key, server_factory=None):
    """Uses one ChatGPT usage limit reset through the Codex CLI's own app-server, only when it is signed in to the
    account OpenClaw uses. `key` makes a repeated click the same request. Returns the outcome Codex reports."""
    with (server_factory or CodexAppServer)(config) as server:
        if not codex_same_account(server, reply):
            raise OwnerError('Use a reset in ChatGPT: this computer cannot check it is the same account')
        result = server.call('account/rateLimitResetCredit/consume', {'idempotencyKey': key})
    outcome = (result or {}).get('outcome')
    if outcome not in ('reset', 'nothingToReset', 'noCredit', 'alreadyRedeemed'):
        raise OwnerError('ChatGPT did not confirm the reset; check it in ChatGPT')
    return outcome


def node_bin(config):
    """The Node binary for the helpers: config `node`, else the one next to the `openclaw` CLI, else PATH."""
    if config.get('node'):
        return str(config['node'])
    sibling = Path(config.get('openclaw') or 'openclaw').parent / 'node'
    return str(sibling) if sibling.exists() else 'node'


def telegram_on(config):
    """Telegram is optional: without an owner ID, cards reach the owner through the dashboard app."""
    return bool(str(config.get('telegram_owner') or '').strip())


def telegram_account(config):
    """The OpenClaw Telegram account (bot) that talks to the owner: config `telegram_account`."""
    return str(config.get('telegram_account') or 'default')


def node_env(config):
    """Environment for the Node helpers: where OpenClaw is installed and who the owner is."""
    env = dict(os.environ)
    if config.get('database'):
        env.setdefault('PUSH_VAPID_FILE', str(Path(config['database']).expanduser().parent / 'vapid.json'))
    if config.get('openclaw_package_dir'):
        env['OPENCLAW_PACKAGE_DIR'] = str(Path(config['openclaw_package_dir']).expanduser())
    if config.get('telegram_owner'):
        env['ASSISTANT_TELEGRAM_OWNER'] = str(config.get('telegram_owner'))
    env['ASSISTANT_TELEGRAM_ACCOUNT'] = telegram_account(config)
    if config.get('dashboard_host'):
        env['PUSH_VAPID_SUBJECT'] = 'https://' + config['dashboard_host'] + config.get('dashboard_path', '/')
    return env
