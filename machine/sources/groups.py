"""Connections, + Add: the groups its list shows the sources in, in order (the dashboard's CONNECT_GROUPS names them)."""
from __future__ import annotations

GROUPS = ('mail', 'chat', 'meetings', 'docs', 'customers', 'work', 'other')
GROUP_OF = {'gmail': 'mail', 'calendar': 'mail', 'outlook': 'mail', 'outlook_calendar': 'mail', 'imap': 'mail',
            'slack': 'chat', 'teams': 'chat', 'whatsapp': 'chat', 'telegram': 'chat', 'linkedin': 'chat', 'x': 'chat',
            'zoom': 'meetings', 'google_meet': 'meetings', 'docs': 'docs',
            'salesflare': 'customers', 'salesforce': 'customers', 'intercom': 'customers', 'stripe': 'customers',
            'github': 'work', 'shortcut': 'work', 'trello': 'work'}


def group_of(service, own=None):
    """A source's group: its own from GROUP_OF, else the one its connector names (`own`, SETUP['group']), else Other."""
    return GROUP_OF.get(service) or (own if own in GROUPS else 'other')
