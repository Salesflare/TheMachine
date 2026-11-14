"""Subscriptions and trials, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

The template's own run (subs_template_run, from mail_cleanup_app.routine_template_run), every month: plain code finds
the candidates (subscriptions.scan) and leaves out what the owner decided (subscriptions.fresh); none ends the run as
nothing new, without a model. Else one small model call confirms and labels them (subs_pass: the background model, no
agent, no tools), once the usage budget allows like any background turn. What it confirms, checked against the mail,
becomes one to-do, quiet like the cleanup to-dos: it waits in the list and the morning summary, no buzz. A new monthly
to-do replaces the open one. A test run only shows its rows.

Between monthly runs, a daily check (subs_soon_step, from routines_app.routines_worker) does the same in plain code
over a shorter look back, for a trial that converts or a renewal that charges within SOON_DAYS and wasn't on a to-do
with that date: only then a model call, and a to-do with just those. Nothing due: no model, no to-do.

Each row is Work or Personal by what it is (a SaaS tool the company pays for is Work); the to-do is Work only when every
row is, so a Personal row never lands in a Work to-do.

On the to-do (subs_pick): Keep or Cancel per row, remembered (subscriptions.pick). Cancel only hands the owner a draft
to the merchant, or the merchant's cancel page: nothing is sent, opened or changed here. The draft goes out only from
the send dialog, on the owner's own Send (todos-subs.js, todos-compose.js)."""
import datetime as dt
import json
import logging

import graph
import help_chat
import i18n
import routine_templates
import routines
import subscriptions
import todo_areas
from machine import todo_states
from machine.store import outcomes
from models import background_model

LOG = logging.getLogger('personal-assistant')
SUBS_TIMEOUT = 120  # seconds the model call may take
SOON_EVERY = 20 * 3600  # the daily check: about once a day


class SubscriptionsApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {
        'subs_pick': 'subs_pick_action',
    }

    # --- the owner's taps ----------------------------------------------------------------------------------------

    def subs_pick_action(self, name, args, owner_dashboard):
        """Keep, Cancel, or none to take it back, on a row. Cancel returns the draft to show (subscriptions.draft):
        nothing is sent or changed."""
        if not owner_dashboard:
            raise ValueError('Only the owner decides this, on the dashboard')
        choice = args.get('choice') or None
        try:
            n = int(args.get('item'))
        except (TypeError, ValueError):
            raise ValueError(i18n.t('That subscription is gone')) from None
        sid = str(args.get('suggestion_id') or '')
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            subscriptions.ensure(db)
            rows = self.subs_rows(db, sid)
            row = subscriptions.pick(db, sid, n, choice, self.routines_stamp(), rows)
        out = {'saved': True, 'choice': choice}
        if choice == 'cancel':
            out['draft'] = subscriptions.draft(row, graph.person_name(self.config.get('owner_name')).strip()[:80])
        return out

    @staticmethod
    def subs_rows(db, suggestion_id):
        """The rows a Subscriptions to-do was made with (its event's metadata)."""
        row = db.execute('SELECT event_ids FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
        if not row:
            return []
        ids = json.loads(row[0] or '[]')
        for (meta,) in db.execute(f"SELECT metadata FROM events WHERE id IN ({','.join('?' * len(ids))})", ids) if ids else ():
            m = subscriptions._meta(meta)
            if m.get('subs'):
                return [r for r in m.get('rows') or () if isinstance(r, dict)]
        return []

    # --- a run -----------------------------------------------------------------------------------------------------

    def subs_found(self, soon=False):
        """The candidates still to ask about, plain code (subscriptions.scan, fresh), and the accounts' areas."""
        accounts = [a['id'] for a in self.cleanup_accounts()]
        now = dt.datetime.now(dt.timezone.utc)
        with self.store.connect() as db:
            subscriptions.ensure(db)
            found = subscriptions.fresh(db, subscriptions.scan(db, accounts, now, soon), soon, self.routines_now().date())
        return found

    def subs_template_run(self, run):
        """The monthly run (routine_template_run): always done here, never an agent turn (True). No candidates: nothing
        new at once, no model. Else the model call in a thread of its own once the usage budget allows."""
        if run['id'] in self.__dict__.get('_routine_steps', ()):
            return True  # its pass is running
        found = self.subs_found()
        if not found:
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                routines.report(db, run['id'], nothing=True, why=i18n.t('No subscriptions to look at'), stamp=self.routines_stamp())
            return True
        now_run = str(run['period']).startswith(('now:', 'test:'))  # the owner pressed it: only the usage limit holds it
        if self.background_pause(owner=now_run, job='routine') or not (now_run or self.background_spaced()):
            return True  # a next step
        self.background_started()
        self.routine_spawn(lambda _: self.subs_pass(run, found), run['id'])
        return True

    def subs_soon_step(self):
        """The daily check between monthly runs: plain code, and a model call and a to-do only for a trial or renewal
        within SOON_DAYS that no to-do showed with that date. Only while the template's routine is on with its own
        words."""
        with self.store.connect() as db:
            routine = routine_templates.live(db, 'subscriptions')
            if not routine or routine['state'] != 'on' or not routine_templates.own(routine['origin'], routine['instructions'], routines.steps_of(routine)):
                return
            subscriptions.ensure(db)
            if not db.execute("SELECT 1 FROM routine_runs WHERE routine_id=? AND state IN ('ready','nothing')", (routine['id'],)).fetchone():
                return  # its first run looks at everything
            db.execute('BEGIN IMMEDIATE')
            if not subscriptions.soon_due(db, dt.datetime.now(dt.timezone.utc), SOON_EVERY):
                return
        found = self.subs_found(soon=True)
        if not found or self.background_pause(owner=False, job='routine') or not self.background_spaced():
            return
        self.background_started()
        self.subs_pass({'id': None, 'routine_id': routine['id'], 'name': routine['name'], 'period': 'soon'}, found, soon=True)

    def subs_ask(self, prompt):
        ask = getattr(self, 'subs_model', None)  # tests and the sandbox: (prompt) -> reply
        try:
            if ask:
                return ask(prompt)
            model = background_model(self.config)
            return help_chat.openclaw_model_run(self.config, prompt, '/'.join(model) if model else None, timeout=SUBS_TIMEOUT)
        except help_chat.Unavailable:
            return None

    def subs_pass(self, run, found, soon=False):
        """The one model call over the candidates; what it confirms, checked against the mail, becomes the to-do after
        the run is settled. None confirmed: nothing new, no to-do. A reply that isn't one: didn't work."""
        areas = {}
        for c in found:
            account = self.cleanup_account(c['account'])
            areas[c['id']] = 'personal' if not account or todo_areas.area_of_account(account) == todo_areas.PERSONAL else 'work'
        text = self.subs_ask(subscriptions.prompt(found, areas))
        answer = subscriptions.reply(text)
        rows = subscriptions.confirmed(found, answer, self.routines_now().date()) if answer is not None else []
        stamp = self.routines_stamp()
        test = run['id'] is not None and routines.is_test(run)
        if run['id'] is not None:
            with self.store.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                if answer is None:
                    routines.finish(db, run['id'], 'failed', stamp, error='no_result' if text else 'runtime_error')
                    return
                if not rows:
                    routines.report(db, run['id'], nothing=True, why=i18n.t('No subscriptions to look at'), stamp=stamp)
                else:
                    routines.report(db, run['id'], text='\n'.join('- ' + subscriptions.line(r) for r in rows) if test
                                    else i18n.t('Found {} subscriptions to look at.', len(rows)), stamp=stamp)
        if rows and not test and not self.subs_todo(run, rows, soon) and run['id'] is not None:
            with self.store.connect() as db:
                routines.restate(db, run['id'], 'failed', i18n.t('Couldn’t make the to-do. The next run tries again.'))

    def subs_todo(self, run, rows, soon=False):
        """The one to-do with its rows. Work only when every row is; a monthly one replaces the open one. Returns its
        id, or None."""
        accounts = self.config.get('accounts', [])
        work = all(r['area'] == 'work' for r in rows)
        mine = [self.cleanup_account(r['account']) for r in rows]
        account = next((a for a in mine if a and (todo_areas.area_of_account(a) != todo_areas.PERSONAL) == work), None) \
            or next((a for a in mine if a), None)
        if not account:
            return None
        area = todo_areas.area_of_account(account)
        companies = todo_areas.companies(accounts)
        title = i18n.t('A trial or renewal charges this week') if soon else i18n.t('Subscriptions to review')
        text = '\n'.join([i18n.t('Keep or cancel each one. Nothing is sent or changed without your OK.'), ''] +
                         ['- ' + subscriptions.line(r)[:160] for r in rows])[:700]
        source = f'routine-subs:{run["id"] or "soon-" + self.routines_stamp()[:10]}'
        with self.store.connect() as db:
            older = [] if soon else subscriptions.open_todos(db)
        event_id = self.store.reviewed_event(account['id'], source, subscriptions.KIND, title, text,
                                             {'sender_display': run.get('name') or i18n.t('Subscriptions and trials'),
                                              'routine': run['routine_id'], 'subs': True, 'rows': rows})
        try:
            sid = self.store.suggest(source, title, text, [event_id], when='now', company=area if work and area in companies else None,
                                     work=work, personal=not work)['id']
        except ValueError as error:
            LOG.warning('subscriptions to-do not saved rows=%d error=%s', len(rows), type(error).__name__)
            return None
        with self.store.connect() as db:
            subscriptions.ensure(db)
            subscriptions.record(db, sid, rows, self.routines_stamp())
            reason, stamp = i18n.t('newer list'), self.routines_stamp()
            for old in older:  # closes by itself, not as the owner's Done: "Closed by itself: newer list", with Undo
                row = db.execute(f"SELECT * FROM suggestions WHERE id=? AND status NOT IN {todo_states.sql(todo_states.CLOSED)}", (old,)).fetchone()
                if old == sid or not row or db.execute('SELECT 1 FROM decisions WHERE id=?', ('subs-replaced:' + old,)).fetchone():
                    continue
                outcomes.close_replaced(db, row, 'subs-replaced:' + old, reason, stamp)
        return sid
