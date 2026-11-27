"""Notes from the owner's older email, the App's part: a domain mixin of App (only machine/main.py composes it;
docs/code-map.md).

From the service's ten-minute step, after the first look, once a connection's history and its live sync are all in,
one bounded pass reads what the owner wrote in that history and keeps how they work as notes on Learning
(history_notes.py). It waits for the usage budget and the gap between background turns like every other
(model_budget, background_pause), runs on the background model in its own thread, and never makes a to-do, a promise
or a reply."""
import logging
import threading

import help_chat
import history_notes
from timeutil import clock, local_tz

LOG = logging.getLogger('personal-assistant')
TRIES = 3  # passes that failed on the same connections before they are left alone


class HistoryNotesApp:
    ACTIONS = {}

    def history_notes_step(self, helpers):
        """Start a pass when one is due and the budget allows; it runs in its own thread. True when started.
        helpers: {'model'}: assistant.py's background_model (a mixin never loads assistant.py)."""
        running = getattr(self, 'history_notes_thread', None)
        if running and running.is_alive():
            return False
        accounts = self.config.get('accounts') or []
        with self.store.connect() as db:
            due = history_notes.due(db, accounts, self.config) if self.store.first_magic_done(db) else []
        if not due or self.background_pause(job='history-notes') or not self.background_spaced():
            return False
        self.background_started()
        self.history_notes_thread = threading.Thread(target=self.history_notes_run, args=(due, helpers), daemon=True, name='history-notes')
        self.history_notes_thread.start()
        return True

    def history_notes_run(self, account_ids, helpers=None, ask=None):
        """One pass over these connections: each model turn outside any connection, the notes saved together, and the
        connections marked read. A pass that fails is tried again on a later step."""
        ask = ask or getattr(self, 'history_notes_model', None)  # tests and the sandbox: (prompt) -> reply
        if ask is None:
            model = (helpers or {})['model'](self.config)

            def ask(prompt):
                return help_chat.openclaw_model_run(self.config, prompt, '/'.join(model) if model else None, timeout=history_notes.TIMEOUT)
        today = f'{clock(local_tz()):%B %d, %Y}'
        try:
            found = history_notes.run(self.store, self.config.get('accounts') or [], account_ids, self.owner_emails(), today, ask)
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                history_notes.mark_read(db, account_ids, found)
        except Exception as error:  # noqa: BLE001 - a pass that fails is tried again later, TRIES times; nothing depends on it
            if isinstance(error, help_chat.Unavailable):  # the model isn't there now: a later step tries again
                LOG.info('history notes: the model is not there, tried again later')
                return {'error': 'Unavailable'}
            tries = self.__dict__.setdefault('history_notes_tries', {})
            key = tuple(account_ids)
            tries[key] = tries.get(key, 0) + 1
            LOG.info('history notes error=%s try=%s', type(error).__name__, tries[key])
            if tries[key] >= TRIES:
                with self.store.connect() as db:
                    db.execute('BEGIN IMMEDIATE')
                    history_notes.mark_read(db, account_ids, {'error': type(error).__name__})
            return {'error': type(error).__name__}
        LOG.info('history notes read=%s turns=%s kept=%s dropped=%s', found['read'], found['turns'], len(found['items']),
                 ','.join(f'{k}:{v}' for k, v in sorted(found['dropped'].items())))
        return found
