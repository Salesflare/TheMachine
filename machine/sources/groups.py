"""Connections, + Add: the groups its list shows the sources in, in order (the dashboard's CONNECT_GROUPS names them)."""
from __future__ import annotations

# mail is Email, calendar is Calendar: a source sits in the one it reads (Exchange Server reads meetings only: Calendar)
GROUPS = ('mail', 'calendar', 'chat', 'meetings', 'docs', 'customers', 'work', 'other')
GROUP_OF = {'gmail': 'mail', 'outlook': 'mail', 'imap': 'mail',
            'calendar': 'calendar', 'outlook_calendar': 'calendar', 'icloud_calendar': 'calendar', 'caldav': 'calendar',
            'proton_calendar': 'calendar', 'ics': 'calendar', 'exchange': 'calendar',
            'slack': 'chat', 'teams': 'chat', 'whatsapp': 'chat', 'telegram': 'chat', 'signal': 'chat', 'linkedin': 'chat', 'x': 'chat',
            'zoom': 'meetings', 'google_meet': 'meetings', 'docs': 'docs', 'google_docs': 'docs',
            'salesflare': 'customers', 'salesforce': 'customers', 'intercom': 'customers', 'stripe': 'customers',
            'github': 'work', 'shortcut': 'work', 'trello': 'work'}
# Catch-all sources ("Other email": any other mail provider): last in their group, after the A to Z rows, in + Add and on
# the Connections tabs (the source's `last`). A new catch-all is added here, never matched by its name.
CATCH_ALL = frozenset({'imap', 'caldav', 'ics'})  # Other email, Other calendar, Calendar link (ICS)


def group_of(service, own=None):
    """A source's group: its own from GROUP_OF, else the one its connector names (`own`, SETUP['group']), else Other."""
    return GROUP_OF.get(service) or (own if own in GROUPS else 'other')


def last(service):
    """True for a catch-all source, shown after the others in its group."""
    return service in CATCH_ALL
