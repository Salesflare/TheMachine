"""Trips, the App's part: booking mail without structured data read by a small model call (bookings.extract_prompt),
so a holiday home, a parking, a rail ticket or a forwarded confirmation lands on its trip too (trip_notes.py has the
rules). A mixin of assistant.App (APP_MIXINS); NotesApp.trip_notes_step builds the trips from what it keeps."""
import datetime as dt
import threading
import time

import bookings
import portable
import trip_notes
from machine.config import LOG
from models import background_model
from timeutil import now

EXTRACT_SECONDS = 600  # how often it looks for booking mail waiting
EXTRACT_MAILS = 6  # mails per call: one call reads a few confirmations, a few thousand tokens in all
EXTRACT_CALLS_DAY = 12  # calls a day at most: a year of held mail is read over a few days, never in one burst
EXTRACT_TURN_SECONDS = 180
SPACED_WAIT_SECONDS = 1800  # after this long waiting for space after other background turns, it goes anyway (within the budget)


class TripsApp:
    ACTIONS = {}

    def trip_extract_step(self, every=EXTRACT_SECONDS):
        """About every ten minutes: when booking mail without structured data waits (trip_notes.queue), one call reads a
        few of them, in a thread of its own, within the usage budget like every background turn. True when one started."""
        if time.monotonic() - self.__dict__.get('trip_extract_at', -every) < every:
            return False
        self.trip_extract_at = time.monotonic()
        thread = getattr(self, '_trip_extract_thread', None)
        if thread and thread.is_alive():
            return False
        today = dt.datetime.fromisoformat(now()).date().isoformat()
        with self.store.connect() as db:
            if not trip_notes.waiting(db):
                return False
        day, calls = self.__dict__.get('trip_extract_calls', (today, 0))
        if (day == today and calls >= EXTRACT_CALLS_DAY) or self.background_pause(job='trip-extract'):
            return False
        waiting = self.__dict__.setdefault('trip_extract_waiting', time.monotonic())
        if not self.background_spaced() and time.monotonic() - waiting < SPACED_WAIT_SECONDS:
            return False
        self.__dict__.pop('trip_extract_waiting', None)
        self.trip_extract_calls = (today, (calls if day == today else 0) + 1)
        self.background_started()
        self._trip_extract_thread = threading.Thread(target=self.trip_extract_run, name='trip-extract', daemon=True)
        self._trip_extract_thread.start()
        return True

    def trip_extract_ask(self, text):
        stand_in = getattr(self, 'trip_extract_model', None)  # tests and the sandbox: (prompt) -> reply
        if stand_in:
            return stand_in(text)
        import help_chat
        swap = background_model(self.config)  # never the costliest model for background work
        return help_chat.openclaw_model_run(self.config, text, '/'.join(swap) if swap else None, timeout=EXTRACT_TURN_SECONDS)

    def trip_extract_run(self):
        """One call over the newest mails waiting; what it reads is kept and the trips follow (trip_notes_step).
        Returns how many mails had bookings."""
        import help_chat
        with self.store.connect() as db:
            mails = trip_notes.pending(db, EXTRACT_MAILS)
        if not mails:
            return 0
        owner = self.config.get('owner_name') or portable.owner_name()  # whose bookings are theirs, not a colleague's
        text = bookings.extract_prompt([{**m, 'id': str(m['id'])} for m in mails], owner)
        try:
            found = bookings.parse(self.trip_extract_ask(text), [str(m['id']) for m in mails])
        except help_chat.Unavailable:
            LOG.info('trip extract: no model now')
            return 0  # nothing counted: the next round asks again
        except (OSError, ValueError, TypeError) as failure:
            LOG.warning('trip extract error=%s', type(failure).__name__)
            found = None
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            kept = trip_notes.answered(db, mails, found, now())
        if kept:
            self.trip_bookings_added = True  # trip_notes_step brings the trips and events up to date
        LOG.info('trip extract mails=%d kept=%d answered=%s', len(mails), kept, found is not None)
        return kept
