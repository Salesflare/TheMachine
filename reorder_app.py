"""Reorders, the App's part: its routine template (routine_templates.Template), listed in machine/main.py's
ROUTINE_TEMPLATES (docs/code-map.md).

Its run (run, from routines_app.routine_template_run), every morning: plain code lists the Shopify stores' order mail
not read yet (reorder.candidates). Only when there is any does one small model call (reorder_pass: the background
model, no agent, no tools) read it, once the usage budget allows like any background turn; what holds up against the
mail is kept as purchases. Then plain code finds the items due again (reorder.due) and makes one quiet to-do per item:
it waits in the list and the morning summary, no buzz. An item ordered again closes its open to-do by itself. A test
run only lists what is due.

Each to-do is Work or Personal by what the order was for (the model's area). Its link opens the store (reorder.way):
nothing is bought here, so Do it is refused (todo_kinds.py) until a Shop connection can check out."""
import datetime as dt
import logging

import help_chat
import i18n
import reorder
import routine_templates
import routines
import todo_areas
from machine.store import outcomes
from models import background_model
import timeutil

LOG = logging.getLogger('personal-assistant')
REORDER_TIMEOUT = 120  # seconds the model call may take


class ReorderTemplate(routine_templates.Template):
    KEYS = ('reorder',)
    KIND = 'reorder'

    def run(self, run, key):
        """A Reorders run (routine_template_run): always done here, never an agent turn (True). No order mail to read:
        only plain code, no model. Else the model call in a thread of its own once the usage budget allows."""
        if run['id'] in self.app.__dict__.get('_routine_steps', ()):
            return True  # its pass is running
        found = self.reorder_found()
        if not found:
            self.reorder_finish(run)
            return True
        now_run = str(run['period']).startswith(('now:', 'test:'))  # the owner pressed it: only the usage limit holds it
        if self.background_pause(owner=now_run, job='routine') or not (now_run or self.background_spaced()):
            return True  # a next step
        self.background_started()
        self.routine_spawn(lambda _: self.reorder_pass(run, found), run['id'])
        return True

    def reorder_found(self):
        accounts = [a['id'] for a in self.cleanup_accounts()]
        with self.store.connect() as db:
            reorder.ensure(db)
            return reorder.candidates(db, accounts, timeutil.clock()) if accounts else []

    def reorder_ask(self, prompt):
        ask = getattr(self, 'reorder_model', None)  # tests and the sandbox: (prompt) -> reply
        try:
            if ask:
                return ask(prompt)
            model = background_model(self.config)
            return help_chat.openclaw_model_run(self.config, prompt, '/'.join(model) if model else None, timeout=REORDER_TIMEOUT)
        except help_chat.Unavailable:
            return None

    def reorder_pass(self, run, found):
        """The one model call over the new order mail; what holds up is kept, then the run ends as reorder_finish. A
        reply that isn't one: didn't work, and the next run reads the same mail again."""
        areas = {}
        for c in found:
            account = self.cleanup_account(c['account'])
            areas[c['id']] = 'personal' if not account or todo_areas.area_of_account(account) == todo_areas.PERSONAL else 'work'
        text = self.reorder_ask(reorder.prompt(found, areas))
        answer = reorder.reply(text)
        if answer is None:
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                routines.finish(db, run['id'], 'failed', self.routines_stamp(), error='no_result' if text else 'runtime_error')
            return
        if not routines.is_test(run):
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                reorder.record(db, found, reorder.confirmed(found, answer), self.routines_stamp())
        self.reorder_finish(run)

    def reorder_finish(self, run):
        """Plain code: close what was ordered again, make a to-do per item due, and the run's result."""
        today, stamp, test = self.routines_now().date(), self.routines_stamp(), routines.is_test(run)
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            reorder.ensure(db)
            if not test:
                for row, day in reorder.bought_again(db):
                    outcomes.close_replaced(db, row, 'reorder-bought:' + row['id'], i18n.t('ordered again'), stamp)
            due = reorder.due(db, today)
        if test:
            made = [reorder.text(d)[0] for d in due]
        else:
            made = [d['row']['title'] for d in due if self.reorder_todo(d)]
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if made:
                routines.report(db, run['id'], text='\n'.join('- ' + m for m in made), stamp=self.routines_stamp())
            else:
                routines.report(db, run['id'], nothing=True, why=i18n.t('Nothing due for a reorder'), stamp=self.routines_stamp())

    def reorder_todo(self, found):
        """One item's to-do, quiet, Work or Personal by the order; its id, or None when it couldn't be made."""
        title, body = reorder.text(found)
        row, work = found['row'], found['row']['area'] == 'work'
        until = found['last'] + dt.timedelta(days=2 * found['usual'])
        try:
            saved = self.store.suggest(f"{reorder.KEY}{found['store']}:{found['item']}:{found['last'].isoformat()}"[:300], title, body,
                                       [row['event_id']], 'now', work=work, personal=not work, quiet=True,
                                       expires_at=until.isoformat(), expires_what=i18n.t('the reorder of {}', row['title'])[:80])
        except ValueError as error:
            LOG.info('reorder to-do not saved error=%s', type(error).__name__)
            return None
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            reorder.save(db, saved['id'], found, self.routines_stamp())
        return saved['id']
