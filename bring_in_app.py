"""Bring these in, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

From the service's ten-minute step, at most once a day and only when OpenClaw's MEMORY.md or USER.md holds lines no
pass has read, one small background turn picks the lines worth keeping as facts (bring_in.py). It waits for the usage
budget and the gap between background turns like every other (model_budget, background_pause), runs on the background
model, and never writes a file or a fact: it only keeps candidates, which the owner ticks on Learning."""
import logging
import threading

import bring_in
import help_chat
from machine.config import WORKSPACE

LOG = logging.getLogger('personal-assistant')


class BringInApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action). The owner's
    # own ticks, from the dashboard only.
    ACTIONS = {'bring_in_decide': 'bring_in_action'}

    def bring_in_workspace(self):
        return getattr(self, 'bring_in_dir', None) or WORKSPACE  # tests and the sandbox point it at their own folder

    def bring_in_action(self, name, args, owner_dashboard):
        if not owner_dashboard:
            raise ValueError('Only the owner brings notes in, on the dashboard')
        done = bring_in.decide(self.store, args.get('keep'), args.get('dismiss'))
        return {**done, 'bring_in': bring_in.status(self.store.connect)}

    def bring_in_step(self, helpers):
        """Start a pass when one is due and the budget allows; it runs in its own thread. True when started.
        helpers: {'model'}: assistant.py's background_model (a mixin never loads assistant.py)."""
        running = getattr(self, 'bring_in_thread', None)
        if running and running.is_alive():
            return False
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if not (self.store.first_magic_done(db) and bring_in.due(db, self.bring_in_workspace(), self.config)):
                return False
        if self.background_pause(job='bring-in') or not self.background_spaced():
            return False
        self.background_started()
        self.bring_in_thread = threading.Thread(target=self.bring_in_run, args=(helpers,), daemon=True, name='bring-in')
        self.bring_in_thread.start()
        return True

    def bring_in_run(self, helpers, ask=None):
        """One pass: the lines and prompt read in one short read, the model turn outside any connection, then saved."""
        ask = ask or getattr(self, 'bring_in_model', None)  # tests and the sandbox: (prompt) -> reply
        try:
            with self.store.connect() as db:
                state = bring_in.prepare(db, self.bring_in_workspace(), self.config)
            if not state['prompt']:
                return {'offered': 0}
            if ask is None:
                model = helpers['model'](self.config)
                reply = help_chat.openclaw_model_run(self.config, state['prompt'], '/'.join(model) if model else None, timeout=bring_in.TIMEOUT)
            else:
                reply = ask(state['prompt'])
        except help_chat.Unavailable:
            reply = None
        except Exception as error:  # noqa: BLE001 - a pass that fails is tried again another day; nothing depends on it
            LOG.info('bring-in pass error=%s', type(error).__name__)
            return {'error': type(error).__name__}
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            found = bring_in.conclude(db, state, reply)
        LOG.info('bring-in pass status=%s offered=%s', found.get('error') or 'ok', found.get('offered', 0))
        return found
