"""Training on the owner's chats. A personal AI plan lets its provider train on chats by default: ChatGPT Free, Go,
Plus and Pro ("Improve the model for everyone"), Claude Free, Pro and Max ("Help improve Claude"). Settings, Model
asks once, in one quiet line, to turn that off, with a link to the provider's own setting; Done hides it for good
(config.json `ai_training_off`, the providers it was done for). Business, Team, Enterprise and Edu plans, API keys,
other providers and local models have nothing to ask, and neither has a plan whose kind is unknown.

state() is in the Machine's status (`ai_training`), so the account can say owners are asked: todo, done or na."""
import json
import re
import shutil
import subprocess
import time
from pathlib import Path

LAYER = 0  # whether the owner's AI plan trains on chats, and where to turn that off (a leaf)

# Where each provider keeps the switch (checked 2026-11): ChatGPT's Settings, Data controls; Claude's Settings, Privacy
SETTINGS = {'chatgpt': 'https://chatgpt.com/settings/data-controls',
            'claude': 'https://claude.ai/settings/data-privacy-controls'}
# The personal plans whose provider trains on chats unless the owner turns it off
PERSONAL = {'chatgpt': {'free', 'go', 'plus', 'pro'}, 'claude': {'free', 'pro', 'max'}}
CLAUDE_PLAN_SECONDS = 3600
_claude_plan = {'at': 0.0, 'plan': None}


def plan_kind(plan):
    """A plan's kind in lower case, from how a provider names it: 'plus', 'Max (20x)', 'self_serve_business' -> 'plus',
    'max', 'business'. None when there is none."""
    words = re.findall(r'[a-z]+', re.sub(r'^self_serve_', '', str(plan or '').strip().lower()))
    return words[0] if words else None


def claude_plan(config, run=subprocess.run, clock=time.time):
    """The kind of plan Claude Code is signed in to, from `claude auth status --json` (it prints no secrets; only
    subscriptionType is kept). Read at most once an hour; None when there is no Claude Code or it can't tell."""
    if clock() - _claude_plan['at'] < CLAUDE_PLAN_SECONDS:
        return _claude_plan['plan']
    found = config.get('claude') or shutil.which('claude')
    local = Path.home() / '.local' / 'bin' / 'claude'
    binary = found or (str(local) if local.exists() else None)
    plan = None
    if binary:
        try:
            data = json.loads(run([str(binary), 'auth', 'status', '--json'], capture_output=True, text=True, timeout=30).stdout)
            if isinstance(data, dict) and data.get('loggedIn'):
                plan = plan_kind(data.get('subscriptionType'))
        except (OSError, ValueError, subprocess.TimeoutExpired):
            plan = None
    _claude_plan.update(at=clock(), plan=plan)
    return plan


def done_for(config, config_path=None):
    """The providers the owner pressed Done for. Read from config.json on disk when there is one: the hosted setup
    page can mark it there too."""
    found = config.get('ai_training_off')
    if config_path:
        try:
            found = json.loads(Path(config_path).read_text()).get('ai_training_off', found)
        except (OSError, ValueError, AttributeError):
            pass
    return {p for p in found if p in SETTINGS} if isinstance(found, list) else set()


def state(status, done=()):
    """For the plan Settings, Model shows (`status`, model_usage.model_status): {'state': 'todo' or 'done', 'provider',
    'url'} for a personal plan, else {'state': 'na'}."""
    status = status or {}
    provider = 'chatgpt' if status.get('chatgpt') else 'claude' if status.get('claude_plan') else None
    if not provider or plan_kind(status.get('plan')) not in PERSONAL[provider]:
        return {'state': 'na'}
    return {'state': 'done' if provider in done else 'todo', 'provider': provider, 'url': SETTINGS[provider]}
