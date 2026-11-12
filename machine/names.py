"""What the owner calls a service, an app or an agent: the one place a key from data becomes a name on screen.

Accounts, jobs and errors carry internal keys: a service ('gmail'), a transport ('gog', 'wacli-local', 'broker'), an
agent tool ('codex'). Owners know Gmail, WhatsApp and Codex, never the command-line tools The Machine runs underneath
(gog, wacli, himalaya, msgraph-cli, the OpenClaw feed). Every owner-facing line that shows such a key goes through
service_name() or agent_name() here, so an internal tool name never reaches the owner as is. Internal identifiers,
config keys and logs keep their names; only what is shown changes.
"""
from __future__ import annotations

import re

SERVICES = {'gmail': 'Gmail', 'calendar': 'Google Calendar', 'outlook': 'Outlook', 'outlook_calendar': 'Outlook Calendar', 'imap': 'Email', 'icloud_calendar': 'iCloud Calendar', 'caldav': 'Calendar',
            'proton_calendar': 'Proton Calendar', 'ics': 'Calendar', 'exchange': 'Exchange',
            'slack': 'Slack', 'teams': 'Microsoft Teams', 'salesflare': 'Salesflare', 'salesforce': 'Salesforce', 'android': 'Android', 'whatsapp': 'WhatsApp', 'telegram': 'Telegram',
            'linkedin': 'LinkedIn', 'x': 'X', 'intercom': 'Intercom', 'zoom': 'Zoom', 'stripe': 'Stripe', 'github': 'GitHub',
            'trello': 'Trello', 'shortcut': 'Shortcut', 'docs': 'Docs', 'google_meet': 'Google Meet', 'rss': 'RSS',
            'gateway': 'Machine health'}
# An account with no service of its own: its transport says which one (an account without either is Gmail, as in
# config.example.json and everywhere `account.get('service', 'gmail')` reads it)
TRANSPORT_SERVICES = {'gog': 'gmail', 'gogcli': 'gmail', 'wacli': 'whatsapp', 'wacli-local': 'whatsapp',
                      'existing_wacli_local_store': 'whatsapp', 'openclaw-feed': 'android', 'existing_openclaw_feed': 'android',
                      'journald': 'gateway', 'telegram_mirror': 'telegram', 'telegram_mirror_store': 'telegram',
                      'himalaya': 'gmail', 'msgraph': 'outlook', 'msgraph-cli': 'outlook', 'gh': 'github',
                      'linkedin-inbox': 'linkedin', 'x-inbox': 'x', 'salesflare-rest': 'salesflare'}
AGENTS = {'claude': 'Claude Code', 'claude_code': 'Claude Code', 'codex': 'Codex', 'codex-cli': 'Codex', 'codex_cli': 'Codex'}
# Names of the tools and runtimes underneath, which an owner never sees as a service, app or channel name
INTERNAL = re.compile(r'(?i)^(?:gog(?:cli)?|wacli|himalaya|msgraph(?:[-_]cli)?|openclaw|codex[-_]cli|gh|journald|maton|broker|'
                      r'api|rest|existing_\w+|[a-z]+[-_](?:feed|local|inbox|rest|store|mirror))(?:[-_][\w-]*)?$')


def internal(value):
    """True when value is the name of an internal tool or transport, not something the owner knows."""
    return bool(INTERNAL.match(str(value or '').strip()))


def account_service(account):
    """The service key of an account: its own, else what its transport means, else Gmail (the config default)."""
    account = account or {}
    service = str(account.get('service') or '')
    if service:
        return service
    return TRANSPORT_SERVICES.get(str(account.get('transport') or ''), 'gmail')


def service_name(key, default=None):
    """'gmail' -> 'Gmail'. A key nobody named here reads in words ('google_drive' -> 'Google drive'), except an
    internal tool or transport name ('gog', 'wacli-local'), which reads as what it is for, or default."""
    key = str(key or '')
    if key in SERVICES:
        return SERVICES[key]
    if key in TRANSPORT_SERVICES:
        return SERVICES[TRANSPORT_SERVICES[key]]
    if not key or internal(key):
        return default
    return key.replace('_', ' ').replace('-', ' ').capitalize()


# A connection named after a workspace or business rather than an address: where that name is kept
WORKSPACE_FIELDS = {'intercom': 'workspace_name', 'stripe': 'account_name'}
WORKSPACE_IDS = {'intercom': 'workspace_id', 'stripe': 'stripe_account'}  # which workspace or account it is


def account_name(account, accounts=(), default=None):
    """What a connection is called on screen: its own name or address; for one without (an Intercom or Stripe shared
    through a Fleet) what it is, 'Intercom', with its workspace when another connection of that kind reads another
    workspace ('Intercom · Acme'). Else default, else its id: never a raw key where a name can be found."""
    account = account or {}
    own = str(account.get('display_name') or account.get('email') or '').strip()
    if own:
        return own
    service = account_service(account)
    if service in WORKSPACE_FIELDS:
        workspace = ' '.join(str(account.get(WORKSPACE_FIELDS[service]) or '').split())[:60]
        key = WORKSPACE_IDS[service]
        others = any(isinstance(a, dict) and a.get('id') != account.get('id') and account_service(a) == service
                     and a.get(key) and a.get(key) != account.get(key) for a in accounts or ())
        return f'{SERVICES[service]} · {workspace}' if workspace and others else SERVICES[service]
    return default if default is not None else str(account.get('id') or '')


def agent_name(tool, default='The agent'):
    """'codex' -> 'Codex': the agent a job was handed to, never its command-line name."""
    tool = str(tool or '')
    if tool in AGENTS:
        return AGENTS[tool]
    if not tool or internal(tool):
        return default
    return tool.replace('_', ' ').replace('-', ' ').capitalize()


def place(text):
    """A line's 'where' ('Gmail · sam@acme.com') as the owner reads it: each part that is an internal tool name
    ('Gog · sam@acme.com', 'wacli') becomes its service, or goes. For values that come from data as they are."""
    parts = []
    for part in str(text or '').split(' · '):
        part = part.strip()
        if internal(part):
            part = service_name(part.lower()) or ''
        if part and part not in parts:
            parts.append(part)
    return ' · '.join(parts) or None
