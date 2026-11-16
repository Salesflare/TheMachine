"""Procedures, the App's part: a domain mixin of App (only machine/main.py composes it; docs/code-map.md).

A preparation's block of the procedures its to-do touches (procedure_lines, read through recall as `procedures`), a
run's procedure on prepare (procedure_check before the save, procedure_saved after it), a stuck run (procedure_failed),
the check turn for what runs handed in (procedures_step, procedures_run) and Remove under Learning
(procedure_remove). The rules are in procedures.py."""
import logging
import threading

import help_chat
from machine.owner_error import OwnerError
from models import background_model
import procedures
import team_learnings

LOG = logging.getLogger('personal-assistant')


class ProceduresApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {
        'procedure_remove': 'procedure_remove_action',
    }

    def own_domains(self):
        return {str(a.get('email') or '').rpartition('@')[2].lower() for a in self.config.get('accounts') or [] if isinstance(a, dict) and '@' in str(a.get('email') or '')}

    def procedure_lines(self, suggestion_id, job_id=None, learn=False):
        """The procedures for the sites and workflows this to-do touches, as data below the owner's own (and, for a run
        the owner started, how to hand one in). The run's id keeps which it was given, for settle."""
        with self.store.connect() as db:
            picked = procedures.pick(db, suggestion_id, self.own_domains())
            if job_id and picked:
                procedures.record_uses(db, job_id, suggestion_id, [p['id'] for p in picked])
        return procedures.prompt_lines(picked, learn)

    def procedures_left_out(self, job_id):
        """The block didn't fit this run's prompt: what it would have given isn't settled by how the run ends."""
        with self.store.connect() as db:
            procedures.left_out(db, job_id)

    def procedure_check(self, args, outcome, early):
        """Before the save: the run's procedure in its fixed form (ValueError says what to fix), or (None, why it isn't
        kept) for one handed in by a run prepared ahead or one that didn't get its task done."""
        if args.get('procedure') is None:
            return None, None
        item = procedures.clean(args['procedure'])
        if early:
            return None, 'not kept: only a run the owner started keeps a procedure'
        if (outcome or {}).get('state') not in procedures.SUCCESS:
            return None, 'not kept: only a run that got its task done keeps a procedure'
        return item, None

    def procedure_saved(self, suggestion_id, item, outcome):
        """After the save: a run that got its task done settles the procedures it was given, and its own waits for the
        check. Returns what the run is told, or None."""
        if (outcome or {}).get('state') not in procedures.SUCCESS:
            return None
        with self.store.connect() as db:
            procedures.settle(db, suggestion_id, True)
            if not item:
                return None
            row = db.execute('SELECT title FROM suggestions WHERE id=?', (str(suggestion_id),)).fetchone()
            personal = suggestion_id in team_learnings.personal_cards(db, [suggestion_id], self.config.get('accounts') or [])
            names = sorted(set(team_learnings.known_names(db, self.config)) | set(procedures.people_on(db, suggestion_id)), key=lambda n: -len(n[0]))
            procedures.draft(db, suggestion_id, item, row['title'] if row else '', 'personal' if personal else 'work', names)
        return 'kept: after a check it helps later tasks on this site or workflow; Learning shows it'

    def procedure_failed(self, suggestion_id):
        """A run on this to-do got stuck: each procedure it was given counts a failure (procedures.settle)."""
        try:
            with self.store.connect() as db:
                procedures.settle(db, suggestion_id, False)
        except Exception as error:  # noqa: BLE001 - a blocker is saved whatever happens here
            LOG.error('procedure settle error=%s', type(error).__name__)

    def procedures_step(self):
        """Start the check of what runs handed in, when there is some and the budget allows; it runs in its own thread.
        True when started."""
        running = getattr(self, 'procedures_thread', None)
        if running and running.is_alive():
            return False
        with self.store.connect() as db:
            if not procedures.pending(db, 1):
                return False
        if self.background_pause(job='procedures') or not self.background_spaced():
            return False
        self.background_started()
        self.procedures_thread = threading.Thread(target=self.procedures_run, daemon=True, name='procedures')
        self.procedures_thread.start()
        return True

    def procedures_run(self, ask=None):
        """One check turn over the oldest drafts: a model turn of its own, no tools, that never saw the runs
        (procedures.check_page), then what it kept is kept (procedures.conclude)."""
        ask = ask or getattr(self, 'procedures_model', None)  # tests and the sandbox: (page) -> reply
        drafts = []
        try:
            with self.store.connect() as db:
                drafts = procedures.pending(db)
                names = team_learnings.known_names(db, self.config)
            if not drafts:
                return {}
            page = procedures.check_page(drafts)
            if ask:
                reply = ask(page)
            else:
                model = background_model(self.config)
                reply = help_chat.openclaw_model_run(self.config, page, '/'.join(model) if model else None, timeout=procedures.TIMEOUT)
        except help_chat.Unavailable:
            return {'error': 'unavailable'}  # the turn never ran: no try spent
        except Exception as error:  # noqa: BLE001 - an unreadable turn is a try without an answer
            LOG.info('procedures check error=%s', type(error).__name__)
            reply = None
        if not drafts:
            return {}
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            found = procedures.conclude(db, drafts, reply, names)
        LOG.info('procedures check kept=%s dropped=%s waiting=%s', len(found['kept']), found['dropped'], found['waiting'])
        return found

    def procedure_remove_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise OwnerError('Only the owner removes a procedure, on the dashboard')
        with self.store.connect() as db:
            gone = procedures.remove(db, str(args.get('id') or ''))
        if gone is None:
            raise OwnerError('This procedure is already gone.')
        return {'removed': str(args['id'])}
