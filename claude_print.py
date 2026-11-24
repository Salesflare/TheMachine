"""One-shot model turns on a Claude sign-in: Claude Code's own print mode (`claude -p`), the executable and sign-in
OpenClaw's Claude CLI route runs reviews and chats on.

`openclaw infer model run` never takes that route: on a Claude sign-in it looks for an Anthropic API key and fails
("No API key found for provider anthropic"), so Help, the bring-in, the bug check, mail cleanup, notes and
subscriptions all failed there, while reviews ran fine. A Gateway agent turn would work but carries OpenClaw's whole
agent prompt, its tools and workspace files: about 48,000 tokens for a short answer, and tools a one-shot turn must not
have.

So a turn here is Claude Code alone: no tools (`--tools ""`), no MCP servers, no skills or slash commands, no settings
files or CLAUDE.md, a one-line system prompt, nothing saved as a session, run in an empty folder. The prompt goes on
stdin. Claude Code's own sign-in is used the way OpenClaw uses it: the variables OpenClaw clears before it starts
Claude Code (an API key, a base URL, a token) are cleared here too, and the sign-in is never read.

`search` is the same turn with one tool, Claude Code's own web search, for one search (machine/signin_search.py).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

import chat_model
from i18n import t

SYSTEM = 'Do what the message asks. Answer with the requested text only.'
# What OpenClaw's Claude CLI backend clears before it starts Claude Code, so its own sign-in answers (OpenClaw 2026.11)
CLEAR_ENV = ('ANTHROPIC_API_KEY', 'ANTHROPIC_API_KEY_OLD', 'ANTHROPIC_API_TOKEN', 'ANTHROPIC_AUTH_TOKEN', 'ANTHROPIC_BASE_URL',
             'ANTHROPIC_CUSTOM_HEADERS', 'ANTHROPIC_OAUTH_TOKEN', 'ANTHROPIC_UNIX_SOCKET', 'CLAUDE_CODE_API_KEY_FILE_DESCRIPTOR',
             'CLAUDE_CODE_ENTRYPOINT', 'CLAUDE_CODE_OAUTH_REFRESH_TOKEN', 'CLAUDE_CODE_OAUTH_TOKEN',
             'CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR', 'CLAUDE_CODE_USE_BEDROCK', 'CLAUDE_CODE_USE_FOUNDRY',
             'CLAUDE_CODE_USE_VERTEX', 'MAX_THINKING_TOKENS')
# OpenClaw's thinking levels as Claude Code's effort
EFFORT = {'off': 'low', 'minimal': 'low', 'low': 'low', 'medium': 'medium', 'adaptive': 'medium', 'high': 'high',
          'xhigh': 'xhigh', 'max': 'max', 'ultra': 'max'}


class Failed(Exception):
    """Claude Code gave no answer: `str()` is its own message, or why there was none."""


def ref(config, model=None):
    """The Claude model a turn on `model` (else the main model) runs on through Claude Code, or None when it doesn't
    take the Claude CLI route (chat_model.claude_code: `claude-cli/*`, or `anthropic/*` pinned to it)."""
    found = model or chat_model.main(config or {})[0]
    return found if found and chat_model.claude_code(config or {}, found) else None


def binary(config):
    """Claude Code: config.json's `claude`, else the one on PATH, else Anthropic's installer's place; None without it."""
    local = Path.home() / '.local' / 'bin' / 'claude'
    return (config or {}).get('claude') or shutil.which('claude') or (str(local) if local.exists() else None)


def run(config, text, model, thinking=None, timeout=90, call=None):
    """The reply's text for `text`, on the Claude model `model` (a `claude-cli/x` or `anthropic/x` ref). Raises Failed,
    and subprocess.TimeoutExpired past `timeout` seconds."""
    result = _call(config, text, model, ['--output-format', 'json', '--tools', ''], thinking, timeout, call)
    try:
        data = json.loads(result.stdout or '{}')
    except ValueError:
        data = {}
    data = data if isinstance(data, dict) else {}
    answer = data.get('result') if isinstance(data.get('result'), str) else ''
    if result.returncode == 0 and not data.get('is_error') and answer.strip():
        return answer.strip()
    lines = [line for line in str(getattr(result, 'stderr', '') or '').splitlines() if line.strip()]
    raise Failed((answer if data.get('is_error') else '') or ' '.join(lines[-3:]) or 'Claude Code gave an empty answer.')


def _call(config, text, model, how, thinking, timeout, call):
    claude = binary(config)
    if not claude:
        raise Failed(t('Claude Code is not installed.'))
    args = [str(claude), '-p', '--model', model.split('/', 1)[-1], *how, '--system-prompt', SYSTEM, '--strict-mcp-config',
            '--disable-slash-commands', '--no-session-persistence', '--setting-sources', '']
    if EFFORT.get(thinking):
        args += ['--effort', EFFORT[thinking]]
    env = {k: v for k, v in os.environ.items() if k not in CLEAR_ENV}
    with tempfile.TemporaryDirectory(prefix='claude-turn-') as folder:
        try:
            return (call or subprocess.run)(args, input=text, capture_output=True, text=True, timeout=timeout, env=env, cwd=folder)
        except OSError:
            raise Failed(t('Claude Code could not be started.')) from None


def search(config, text, model, timeout=90, call=None):
    """(the reply's text, {address: title} of what the search returned) of a turn whose only tool is Claude Code's web
    search, used once (two model turns: the search, then the answer). Raises Failed when it didn't search or gave no
    answer, and subprocess.TimeoutExpired past `timeout` seconds."""
    result = _call(config, text, model, ['--output-format', 'stream-json', '--verbose', '--tools', 'WebSearch', '--allowedTools', 'WebSearch',
                                         '--max-turns', '2'], None, timeout, call)
    answer, links, searched = '', {}, 0
    for line in str(result.stdout or '').splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        row = row if isinstance(row, dict) else {}
        found = row.get('tool_use_result')
        if isinstance(found, dict) and isinstance(found.get('results'), list):
            searched += 1
            for part in found['results']:
                for hit in part.get('content') or () if isinstance(part, dict) and isinstance(part.get('content'), list) else ():
                    if isinstance(hit, dict) and isinstance(hit.get('url'), str):
                        links[hit['url']] = str(hit.get('title') or '')
        if row.get('type') == 'result' and not row.get('is_error') and isinstance(row.get('result'), str):
            answer = row['result'].strip()
    if result.returncode != 0 or not answer or not searched:
        raise Failed('Claude Code gave no search results.')
    return answer, links
