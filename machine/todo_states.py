"""Every status a to-do (a row of `suggestions`) can have, and the named groups the code asks about. A leaf: it
imports nothing, so any module can use it. Code and SQL name a group here instead of spelling statuses out
(tests/test_architecture.py checks that); a module that means something else names that difference here."""

PENDING = 'pending'            # new, needs the owner
ACCEPTED = 'accepted'          # Do it: The Machine is preparing it
PREPARED = 'prepared'          # ready for the owner's look
INSTRUCTIONS = 'instructions'  # the owner asked for changes: preparing again
SNOOZED = 'snoozed'            # Later: back at snoozed_until
COMPLETED = 'completed'        # done
REJECTED = 'rejected'          # Not needed

ALL = (PENDING, ACCEPTED, PREPARED, INSTRUCTIONS, SNOOZED, COMPLETED, REJECTED)
OPEN = (PENDING, ACCEPTED, PREPARED, INSTRUCTIONS, SNOOZED)  # not closed, snoozed included
OPEN_NOT_SNOOZED = (PENDING, ACCEPTED, PREPARED, INSTRUCTIONS)  # open and awake now
CLOSED = (COMPLETED, REJECTED)
CLOSED_OR_SNOOZED = (COMPLETED, REJECTED, SNOOZED)  # nothing to show or do on it right now
PREPARING = (ACCEPTED, INSTRUCTIONS)  # Do it pressed or changes asked: The Machine is on it
TAKEN_ON = (ACCEPTED, PREPARED, INSTRUCTIONS)  # preparing or prepared
TAKEN = (ACCEPTED, PREPARED, INSTRUCTIONS, COMPLETED)  # fleet: someone took it on or did it, so a teammate's offer is held
WAITING_ON_OWNER = (PENDING, PREPARED)  # the owner's move: not snoozed, closed or still preparing
NOT_STARTED = (PENDING, SNOOZED)  # open, and no Do it asked yet
OPEN_UNPREPARED = (PENDING, ACCEPTED, INSTRUCTIONS, SNOOZED)  # open, and its text is still its own account, not an outcome


def sql(*states):
    """The list for an SQL IN, from groups and single statuses: sql(NOT_STARTED, REJECTED) is
    "('pending','snoozed','rejected')". Only known statuses go in, so the text is safe to put in a query."""
    flat = [s for part in states for s in ((part,) if isinstance(part, str) else part)]
    if not flat or any(s not in ALL for s in flat):
        raise ValueError(f'not a to-do status: {flat!r}')
    return '(' + ','.join(f"'{s}'" for s in flat) + ')'
