"""The missed-work audit, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

Once a week, from the service's ten-minute step, one small background turn judges a sample of reviewed signals that
got no to-do (missed_work.py). It waits for the usage budget and the gap between background turns like every other
(model_budget, background_pause), runs on the background model, and never touches the review, a to-do or a promise:
it only keeps its numbers and the misses it found, which the owner labels on Learning, How it's going."""
import logging
import threading

import missed_work

LOG = logging.getLogger('personal-assistant')


class MissedWorkApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action). The owner's
    # own label on a miss, from the dashboard only.
    ACTIONS = {'missed_work_label': 'missed_work_action'}

    def missed_work_action(self, name, args, owner_dashboard):
        if not owner_dashboard:
            raise ValueError('Only the owner labels a miss, on the dashboard')
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            missed_work.label(db, args.get('event_id'), args.get('label') or None)
        with self.store.connect() as db:
            return {'missed_work': missed_work.summary(db)}

    def missed_work_step(self, helpers):
        """Start the week's audit when it is due and the budget allows; it runs in its own thread. None when not started.
        helpers: {'owned', 'bulk', 'model'}: assistant.py's calendar_owned, bulk_kind and background_model (a mixin never
        loads assistant.py)."""
        running = getattr(self, 'missed_work_thread', None)
        if running and running.is_alive():
            return None
        with self.store.connect() as db:
            if not (missed_work.due(db) and self.store.first_magic_done(db)):
                return None
        if self.background_pause(job='missed-work') or not self.background_spaced():
            return None
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if not missed_work.due(db):
                return None
            audit_id = missed_work.begin(db)
        self.background_started()
        self.missed_work_thread = threading.Thread(target=self.missed_work_run, args=(audit_id, helpers), daemon=True, name='missed-work')
        self.missed_work_thread.start()
        return audit_id

    def missed_work_run(self, audit_id, helpers, ask=None):
        """One audit: the sample and prompt read in one short read, the model turn outside any connection, then saved."""
        try:
            if ask is None:
                model = helpers['model'](self.config)
                ask = lambda prompt: missed_work.model_run(self.config, prompt, '/'.join(model) if model else None)
            own = frozenset(self.owner_emails())
            with self.store.connect() as db:
                state = missed_work.prepare(db, self.config.get('accounts') or [], own=own, seed=audit_id, owned=helpers.get('owned'), bulk=helpers.get('bulk'))
            found = missed_work.conclude(state, None if state.get('error') else ask(state['prompt']))
        except Exception as error:  # noqa: BLE001 - an audit that fails is kept as failed; nothing else depends on it
            found = {'error': type(error).__name__}
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            missed_work.save(db, audit_id, found)
        LOG.info('missed-work audit status=%s', found.get('error') or 'ok')
        return found
