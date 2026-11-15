"""Connections, + Add: the groups its list shows the sources in, in order (the dashboard's CONNECT_GROUPS names them)."""
from __future__ import annotations

from machine import services

# mail is Email, calendar is Calendar: a source sits in the one it reads (Exchange Server reads meetings only: Calendar).
# Each service's group is its row in machine/services.py.
GROUPS = services.GROUPS
GROUP_OF = services.field('group')
# Catch-all sources ("Other email": any other mail provider): last in their group, after the A to Z rows, in + Add and on
# the Connections tabs (the source's `last`). A new catch-all says so in its row, never matched by its name.
CATCH_ALL = frozenset(services.of(flag='last'))  # Other email, Other calendar, Calendar link (ICS)


def group_of(service, own=None):
    """A source's group: its own from GROUP_OF, else the one its connector names (`own`, SETUP['group']), else Other."""
    return GROUP_OF.get(service) or (own if own in GROUPS else 'other')


def last(service):
    """True for a catch-all source, shown after the others in its group."""
    return service in CATCH_ALL
