"""Work or Personal for a sign-in, from its address and what its provider says (onboarding.connect, connect_grant): which
addresses are a mail provider's (company_of), the guess (guess_boundary), the one question when in doubt (ask_scope),
and how a boundary reads (scope_label) or is typed (boundary_label). Out of onboarding.py, which imports these back."""
from __future__ import annotations

import re

# Mail providers, not companies: the names in enrichment.FREEMAIL and a few more (tests check they stay in step)
WEBMAIL = {'gmail', 'googlemail', 'outlook', 'hotmail', 'live', 'msn', 'yahoo', 'ymail', 'rocketmail', 'icloud', 'me', 'mac',
           'aol', 'proton', 'protonmail', 'pm', 'gmx', 'web', 'mail', 'yandex', 'zoho', 'fastmail', 'hey', 'tutanota', 'tuta',
           'qq', '163', '126', 'naver', 'libero', 'wanadoo', 'laposte', 't-online', 'seznam', 'skynet', 'telenet', 'proximus',
           'scarlet', 'pandora', 'ziggo', 'kpnmail', 'xs4all', 'btinternet', 'comcast', 'sbcglobal', 'bigpond'}
# Sources that sign in as an address: Work or Personal comes from that address once it is known (guess_boundary), so
# + Add asks neither. A Google Workspace or Microsoft work address is on the company's own domain; a consumer one is not.
ADDRESS_SCOPE = ('gmail', 'calendar', 'outlook', 'outlook_calendar')
CONSUMER_TENANT = '9188040d-6c67-4c5b-b112-36a304b66dad'  # Microsoft's tenant for Outlook.com accounts (ms_graph.py)
TENANT_ID = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')


def company_of(email):
    """A company name guessed from a work address (alex@acme.io -> Acme, sam@mail.acme.co.uk -> Acme); '' for webmail."""
    parts = str(email or '').rpartition('@')[2].lower().split('.')[:-1]
    if parts and parts[-1] in ('co', 'com', 'org', 'net', 'ac', 'gov') and len(parts) > 1:
        parts = parts[:-1]
    name = parts[-1] if parts else ''
    return '' if not name or name in WEBMAIL or name == 'example' else name.capitalize()


def guess_boundary(config, email, account=None, team_domains=(), tid=None):
    """(boundary, by) for a new sign-in from what is known about its address, or (None, None) when that is too weak to
    guess: then the owner is asked. Sharing follows Work, so a wrong Work guess would share personal mail with a team;
    a doubt is asked, never guessed Work. In order: another account on the same address (the owner's marking travels);
    a mail provider's address, or a Microsoft account in the consumer tenant (tid), is Personal; an address on the
    domain of a Work Fleet teammate is Work. A company's own domain alone is not enough, not even a Google Workspace or
    Microsoft work tenant on it: people use their own domain for personal mail too."""
    email = str(email or '').strip().lower()
    same = [a for a in config.get('accounts', []) if a is not account and str(a.get('email') or '').strip().lower() == email
            and ':' in str(a.get('boundary') or '') and not str(a['boundary']).startswith('owner:')]
    owned = [a for a in same if a.get('boundary_by') == 'owner']
    if owned or same:
        return (owned or same)[0]['boundary'], (owned or same)[0].get('boundary_by') or 'guess'
    company = company_of(email)
    if not company or str(tid or '').lower() == CONSUMER_TENANT:
        return 'personal:me', 'guess'
    if email.rpartition('@')[2] in {str(d).lower() for d in team_domains}:
        return 'work:' + company, 'guess'
    return None, None


def ask_scope(config, account, ui, organization=False):
    """The one Work or Personal question for an address that doesn't say (guess_boundary): Work with the company its
    domain names, or Personal. The owner's own marking. organization: the sign-in is a Google Workspace or Microsoft
    work account (organization_of), so Work comes first; else Personal does."""
    company = company_of(account.get('email')) or 'Main'
    work, personal = ('work:' + company, scope_label('work:' + company)), ('personal:me', 'Personal')
    from onboarding import boundaries  # noqa: PLC0415 - onboarding imports this module
    rest = [(b, scope_label(b)) for b in boundaries(config, account.get('service', 'gmail')) if b not in (work[0], personal[0])]
    options = [work, *rest, personal] if organization else [personal, work, *rest]
    return ui.choose('Is this account work or personal?', list(dict(options).items()))


def organization_of(config, account):
    """Whether the sign-in belongs to an organization, from what its provider says about it with the access it has (no
    other scope): a Microsoft account's tenant (tenant_id; the consumer tenant is not one), a Google account's
    Workspace domain (`hd` in its OpenID user info, which the sign-in's email scope reads). None when unknown."""
    if account.get('service') in ('outlook', 'outlook_calendar'):
        tid = str(account.get('tenant_id') or '').lower()
        return (tid != CONSUMER_TENANT) if TENANT_ID.fullmatch(tid) else None
    try:
        import sources
        info = sources.gog_read(config, account, 'oauth2', 'v2', 'oauth2.userinfo.get', {},
                                'https://www.googleapis.com/auth/userinfo.email')
    except Exception:  # noqa: BLE001 - a hint only: without it the question keeps its plain order
        return None
    return bool(str(info.get('hd') or '').strip()) if isinstance(info, dict) else None


def boundary_label(text, default='work:Main'):
    """work:<Company> or personal:<name> from what someone typed: 'Acme' is work:Acme, 'personal' or 'me'
    is personal:me, and a full label is kept."""
    text = str(text or '').strip()
    kind, colon, name = text.partition(':')
    if colon and kind.strip().lower() in ('work', 'personal', 'owner') and name.strip():
        return f'{kind.strip().lower()}:{name.strip()}'
    if text.lower().rstrip(':') in ('personal', 'private', 'me', 'home', 'family'):
        return 'personal:' + ('family' if text.lower() == 'family' else 'me')
    if text.lower().rstrip(':') in ('', 'work'):
        return default
    return 'work:' + (name.strip() if colon else text)


def ask_boundary(ui, default):
    return boundary_label(ui.ask('Company name, or "personal" (stored as work:<Company> or personal:<name>)', default), default)


def scope_label(boundary):
    """How a boundary reads to the owner: work:Acme is Work · Acme, personal:me is Personal."""
    kind, _, name = str(boundary or '').partition(':')
    if kind == 'work' and name:
        return 'Work · ' + name
    if kind == 'personal':
        return 'Personal' if name in ('', 'me') else 'Personal · ' + name
    return str(boundary or '')
