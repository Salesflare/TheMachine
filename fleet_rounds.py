"""The Fleet's background rounds (fleet.py, Fleet.run): each reads the directory and the owner's own addresses once
instead of on every use, and logs a part that was slow. A mixin of fleet.Fleet."""
from __future__ import annotations

import contextlib
import logging
import threading
import time

LOG = logging.getLogger('personal-assistant')
ROUND_KEEP_SECONDS = 60  # a round's reads of the owner's own addresses hold this long (Rounds.round_reads)
ROUND_LOG_SECONDS = 2.0  # a part of the Fleet's round that takes this long is logged (Rounds.timed)
_ROUND = threading.local()  # this thread's round reads (Rounds.round_reads)


def _thread_read():
    """Bytes this thread has read so far (Linux), for the slow-round log line; None elsewhere."""
    try:
        with open('/proc/thread-self/io') as f:
            return next(int(line.split()[1]) for line in f if line.startswith('rchar'))
    except (OSError, ValueError, StopIteration):
        return None


class Rounds:
    @contextlib.contextmanager
    def round_reads(self):
        """One background round (run): the directory and the owner's own addresses are read once for it instead of on
        every use. A new directory, from any thread, is read again at once (set_meta); the owner's addresses within
        ROUND_KEEP_SECONDS."""
        before = getattr(_ROUND, 'value', None)
        _ROUND.value = {'of': self, 'gen': getattr(self, '_directory_gen', 0), 'at': time.monotonic(), 'meta': {}}
        try:
            yield
        finally:
            _ROUND.value = before

    def _round_memo(self, part='meta'):
        """This thread's round memo (round_reads) while it still holds, else None."""
        kept = getattr(_ROUND, 'value', None)
        if not kept or kept['of'] is not self:
            return None
        if kept['gen'] != getattr(self, '_directory_gen', 0) or time.monotonic() - kept['at'] > ROUND_KEEP_SECONDS:
            kept.update(gen=getattr(self, '_directory_gen', 0), at=time.monotonic(), meta={})
            kept.pop('own', None), kept.pop('domains', None)
        return kept['meta'] if part == 'meta' else kept

    def timed(self, part, fn, *args, **kwargs):
        """fn(*args, **kwargs), with one log line when it took ROUND_LOG_SECONDS or more: which part of the Fleet's
        round, how long and how much it read (what made the Fleet thread busy, 2026-11-10). Never anything it read."""
        began, read = time.monotonic(), _thread_read()
        try:
            return fn(*args, **kwargs)
        finally:
            took = time.monotonic() - began
            if took >= ROUND_LOG_SECONDS:
                after = _thread_read()
                LOG.info('fleet round slow part=%s took=%.1fs read=%s', part, took,
                         f'{(after - read) / 1e6:.0f}MB' if read is not None and after is not None else '-')

    def my_emails(self):
        """The owner's addresses: theirs in the directory, their accounts', and the ones found as theirs here (aliases,
        their calendar; own_addresses.py). The last stay on this Machine: the directory only hears account_emails."""
        import sqlite3
        import own_addresses
        mine = {e for ref in self.work_fleets() for m in self.fleets()[ref].get('members', []) if m.get('me') for e in m.get('emails', [])}
        found, kept = set(), self._round_memo('round')
        if kept is not None and 'own' in kept:
            found = set(kept['own'])  # once per round (round_reads): claims and handled asked for each to-do
        elif self.connect:
            try:
                with self.connect() as db:
                    found = own_addresses.yours(db, self.config)
                if kept is not None:
                    kept['own'] = frozenset(found)
            except sqlite3.Error:
                pass
        return mine | found | {str(a.get('email') or '').lower() for a in self.config.get('accounts', []) if a.get('email')}

    def own_domains(self):
        """The domains the owner added as their company's too (own_addresses.domains): never a client's."""
        import sqlite3
        import own_addresses
        if not self.connect:
            return set()
        kept = self._round_memo('round')
        if kept is not None and 'domains' in kept:
            return set(kept['domains'])
        try:
            with self.connect() as db:
                found = own_addresses.domains(db)
        except sqlite3.Error:
            return set()
        if kept is not None:
            kept['domains'] = frozenset(found)
        return found
