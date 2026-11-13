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
            'slack': 'Slack', 'teams': 'Microsoft Teams', 'salesflare': 'Salesflare', 'salesforce': 'Salesforce', 'android': 'Android', 'whatsapp': 'WhatsApp', 'telegram': 'Telegram', 'signal': 'Signal',
            'linkedin': 'LinkedIn', 'x': 'X', 'intercom': 'Intercom', 'zoom': 'Zoom', 'stripe': 'Stripe', 'github': 'GitHub',
            'trello': 'Trello', 'shortcut': 'Shortcut', 'docs': 'Docs', 'google_meet': 'Google Meet', 'rss': 'RSS',
            'gateway': 'Machine health'}
# An account with no service of its own: its transport says which one (an account without either is Gmail, as in
# config.example.json and everywhere `account.get('service', 'gmail')` reads it)
TRANSPORT_SERVICES = {'gog': 'gmail', 'gogcli': 'gmail', 'wacli': 'whatsapp', 'wacli-local': 'whatsapp',
                      'existing_wacli_local_store': 'whatsapp', 'openclaw-feed': 'android', 'existing_openclaw_feed': 'android',
                      'journald': 'gateway', 'telegram_mirror': 'telegram', 'telegram_mirror_store': 'telegram', 'signal_mirror': 'signal', 'signal_mirror_store': 'signal',
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


# A connection without a name of its own yet: what its card says, not the account id (machine/sources/connectors.py)
UNNAMED = {'trello': 'Trello board', 'gateway': 'Machine health'}
# A config key, not a name: lowercase words joined by - or _ ('personal-signal', 'work_gmail'). Never a card's title.
SLUG = re.compile(r'[a-z0-9]+(?:[-_][a-z0-9]+)+')
# Chat apps on the owner's own phone number: a name the app tells reads as whose it is ("Sam’s Signal")
OWNED_CHATS = ('whatsapp', 'telegram', 'signal')
# A device boundary's name is its kind, not a person or company: personal:signal reads Personal
DEVICE_SCOPES = ('phone', 'device', 'chats', 'chat')
# Where a connection keeps the handle, address or workspace that tells it apart, after its email
HANDLES = (('handle', '@'), ('login', '@'), ('workspace_name', ''), ('account_name', ''), ('workspace', ''), ('username', ''))
TLDS = {'com', 'org', 'net', 'io', 'co', 'ai', 'app', 'dev', 'eu', 'be', 'nl', 'de', 'fr', 'uk', 'us', 'www'}


def _t():
    import i18n
    return i18n.t


def words(text):
    """The words of a name or line, lowercased, without a domain's ending: 'Work · acme.com' -> {'work', 'acme'}."""
    return {w for w in re.findall(r'[^\W_]+', str(text or '').casefold()) if w not in TLDS}


def kind_words(service):
    """The words that only say what kind of connection it is: its key and its names ('signal', 'Signal chats')."""
    import onboarding
    try:
        label = onboarding.label(service)
    except Exception:  # noqa: BLE001 - a connector that can't load still has its key and name
        label = ''
    return words(service) | words(service.replace('_', '')) | words(service_name(service)) | words(label)


def _overlaps(part, title):
    """Whether a subtitle part says what the title says already: a shared word, or one holds the other's letters
    ('TheMachine' under 'The Machine', '@HeyAcme' under 'Acme')."""
    mine = words(part)
    joined = lambda text: re.sub(r'[\W_]+', '', str(text or '').casefold())
    return bool(mine & words(title)) or (len(joined(part)) > 2 and joined(part) in joined(title)) \
        or (len(joined(title)) > 2 and joined(title) in joined(part))


def usable_name(name, account):
    """A name fit for a card: not empty, not the account's id or a config key, not only its kind ('signal')."""
    name = ' '.join(str(name or '').split())[:120]
    service = account_service(account)
    if not name or name == account.get('id') or SLUG.fullmatch(name) or name.casefold() in (service, service.replace('_', ' ')):
        return ''
    # "Acme on X": the logo already says X, so the card says Acme
    provider = SERVICES.get(service)
    if provider:
        name = re.sub(r'\s+(?:on|in)\s+' + re.escape(provider) + r'$', '', name) or name
    return name


def card_title(account, accounts=(), state=None, t=None):
    """A connection card's title: the account's own name as its provider tells it (an X profile's name, a Slack
    workspace, a Telegram or Signal account's owner as "Sam’s Signal"), else the name it was given, else its address.
    Never its id or a config key. Without any, its provider's name, numbered when there are several ('Signal 2')."""
    account, state = account or {}, state or {}
    t = t or _t()
    service = account_service(account)
    provider = SERVICES.get(service) or service_name(service) or 'Connection'
    told = usable_name(state.get('account_name'), account)
    own = usable_name(account.get('display_name'), account)
    if service == 'x' and told:
        return told
    if own:
        return own
    if told:
        return t('{}’s {}', told.split()[0], provider) if service in OWNED_CHATS else told
    for named in (account.get('email'), account.get(WORKSPACE_FIELDS.get(service, 'workspace_name')), account.get('workspace')):
        if usable_name(named, account):  # its address; an Intercom, Stripe or Shortcut by its workspace
            return usable_name(named, account)
    handle = usable_name(account.get('handle'), account)
    if handle:
        return '@' + handle.lstrip('@')
    if service in UNNAMED:
        return UNNAMED[service]
    # several of this kind without a name: told apart by their order
    same = [a.get('id') for a in accounts or () if isinstance(a, dict) and account_service(a) == service]
    at = same.index(account.get('id')) + 1 if account.get('id') in same else 1
    return provider if at == 1 else f'{provider} {at}'


def scope_part(boundary, labels=None, t=None):
    """Work or Personal as a card's subtitle says it: the company's label (work_or_personal.work_labels), Personal
    with a person's name; a device boundary's kind (personal:signal, personal:phone) adds nothing."""
    t = t or _t()
    kind, _, name = str(boundary or '').partition(':')
    if kind == 'work':
        label = str((labels or {}).get(boundary) or ('Work · ' + name if name else 'Work'))
        return re.sub(r'^Work(?= · |$)', t('Work'), label)
    if kind == 'personal':
        plain = not name or name in ('me', 'personal') or name.casefold() in DEVICE_SCOPES or name.casefold() in SERVICES or name.casefold() in TRANSPORT_SERVICES
        return t('Personal') if plain else t('Personal') + ' · ' + name
    return ''  # owner:system, The Machine's own health: neither


def card_detail(account):
    """The one thing that tells this connection apart from another of its kind: its address, handle or workspace."""
    email = str(account.get('email') or '').strip()
    if '@' in email or usable_name(email, account):  # an old install's label kept as email ('the-machine') is not one
        return email
    for key, mark in HANDLES:
        value = ' '.join(str(account.get(key) or '').split())[:80].lstrip('@')
        if value and (mark or not SLUG.fullmatch(value)):  # a handle is one as it is; a workspace key ('acme-eu') is not a name
            return mark + value
    return ''


def account_card(account, accounts=(), state=None, labels=None, t=None):
    """{'card_title', 'card_subtitle'} of a connection's card on Connections: every connector's, the one place they are
    made (tests/test_card_names.py checks each kind in the registry). The subtitle is Work or Personal, and the
    address or handle only when the title doesn't say it already; never the provider's name or kind again (its logo
    and its tab say that), never a raw key, never a word the title has."""
    account = account or {}
    t = t or _t()
    title = card_title(account, accounts, state, t)
    service = account_service(account)
    kinds = kind_words(service)
    company_only = lambda part: part.split(' · ', 1)[1] if ' · ' in part else ''
    scope = scope_part(account.get('boundary'), labels, t)
    parts = []
    if scope:
        extra = company_only(scope)
        head = scope.split(' · ', 1)[0]
        parts.append(head if extra and (_overlaps(extra, title) or words(extra) <= kinds) else scope)
    detail = card_detail(account)
    if detail and not _overlaps(detail, title) and not (words(detail) and words(detail) <= kinds) \
            and not any(_overlaps(detail, p) for p in parts):
        parts.append(detail)
    return {'card_title': title, 'card_subtitle': ' · '.join(p for p in parts if p)}


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
