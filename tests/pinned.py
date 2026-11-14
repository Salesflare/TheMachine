"""Run a test at a chosen moment: `pinned(when)` fixes timeutil.clock(), the one place the app reads the current time,
so a test about "Friday", a snooze, a due date or work hours gives the same answer on any day it runs.

    with pinned('2026-11-09T12:00:00+00:00') as pin:
        ...                       # clock(), today() and now() read 2026-11-09 12:00 UTC
        pin.move(days=4)          # and now the 13th

It is a decorator too (`@pinned(NOW)` on a test method). The clock stays still inside: code that
waits for time to pass moves it with pin.move. `when` is an aware datetime or ISO text with an offset; on leaving, the
clock is put back as it was (a pinned block inside another one returns to the outer moment)."""
import contextlib
import datetime as dt

import timeutil


class Pin:
    def move(self, **delta):
        """Move the pinned clock by a timedelta's keywords (days=1, minutes=-5)."""
        timeutil.pin(timeutil.PINNED + dt.timedelta(**delta))

    @property
    def at(self):
        return timeutil.PINNED


@contextlib.contextmanager
def pinned(when):
    before = timeutil.PINNED
    timeutil.pin(when)
    try:
        yield Pin()
    finally:
        timeutil.PINNED = before
