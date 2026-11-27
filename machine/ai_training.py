"""Training on the owner's chats. A personal AI plan lets its provider train on chats by default: ChatGPT Free, Go,
Plus and Pro ("Improve the model for everyone"), Claude Free, Pro and Max ("Help improve Claude"). Settings, Model
asks once, in one quiet line, to turn that off, with a link to the provider's own setting; Done hides it for good
(config.json `ai_training_off`, the providers it was done for). Business, Team, Enterprise and Edu plans, API keys,
other providers and local models have nothing to ask, and neither has a plan whose kind is unknown.

state() is in the Machine's status (`ai_training`), so the account can say owners are asked: todo, done or na."""
import json
import subprocess
import time
from pathlib import Path

from machine import claude_signin

LAYER = 0  # whether the owner's AI plan trains on chats, and where to turn that off (a leaf)

# Where each provider keeps the switch (checked 2026-11): ChatGPT's Settings, Data controls; Claude's Settings, Privacy
SETTINGS = {'chatgpt': 'https://chatgpt.com/settings/data-controls',
            'claude': 'https://claude.ai/settings/data-privacy-controls'}
# The personal plans whose provider trains on chats unless the owner turns it off
PERSONAL = {'chatgpt': {'free', 'go', 'plus', 'pro'}, 'claude': {'free', 'pro', 'max'}}
# A plan's kind in lower case, from how a provider names it: 'plus', 'Max (20x)', 'self_serve_business' -> 'plus',
# 'max', 'business'. None when there is none.
plan_kind = claude_signin.plan_kind


def claude_plan(config, run=subprocess.run, clock=time.monotonic):
    """The kind of plan Claude Code is signed in to: the same reading of `claude auth status --json` as Needs you's
    (machine/claude_signin.py, at most once an hour while signed in). None when there is no Claude Code or it can't tell."""
    return (claude_signin.read(config, run, clock) or {}).get('plan')


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
