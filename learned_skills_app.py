"""Learned skills, the App's part: a domain mixin of App (only machine/main.py composes it; docs/code-map.md).

A run's procedure on prepare (learned_check before the save, learned_saved after it), a stuck run (learned_failed),
and the check turn for what runs handed in (learned_step, learned_run), which writes what it kept as skills of origin
'learned' (skills.Skills.learn). The rules are in learned_skills.py; the skills table is skills.py's."""
import logging
import threading

import help_chat
import learned_skills
from models import background_model
import team_learnings

LOG = logging.getLogger('personal-assistant')


class LearnedSkillsApp:
    ACTIONS = {}  # no actions of its own: learned skills show, change and go in the Skills list (skills.py)

    def own_domains(self):
        return {str(a.get('email') or '').rpartition('@')[2].lower() for a in self.config.get('accounts') or [] if isinstance(a, dict) and '@' in str(a.get('email') or '')}

    def learned_settle(self, suggestion_id, ok):
        """A run on this to-do ended: the learned skills for the sites and workflows it touches count it."""
        with self.store.connect() as db:
            ids = [r['id'] for r in learned_skills.touching(db, suggestion_id, self.own_domains())]
        return self.skills.learned_result(ids, ok, learned_skills.RETIRE) if ids else []

    def learned_check(self, args, outcome, early):
        """Before the save: the run's procedure in its fixed form (ValueError says what to fix), or (None, why it isn't
        kept) for one handed in by a run prepared ahead or one that didn't get its task done."""
        if args.get('procedure') is None:
            return None, None
        item = learned_skills.clean(args['procedure'])
        if early:
            return None, 'not kept: only a run the owner started teaches a skill'
        if (outcome or {}).get('state') not in learned_skills.SUCCESS:
            return None, 'not kept: only a run that got its task done teaches a skill'
        return item, None

    def learned_saved(self, suggestion_id, item, outcome):
        """After the save: a run that got its task done settles the learned skills it touched, and its own procedure,
        with personal details out, waits in memory for the check. Returns what the run is told, or None."""
        if (outcome or {}).get('state') not in learned_skills.SUCCESS:
            return None
        self.learned_settle(suggestion_id, True)
        if not item:
            return None
        with self.store.connect() as db:
            row = db.execute('SELECT title FROM suggestions WHERE id=?', (str(suggestion_id),)).fetchone()
            names = sorted(set(team_learnings.known_names(db, self.config)) | set(learned_skills.people_on(db, suggestion_id)), key=lambda n: -len(n[0]))
        task = learned_skills.scrub_text(row['title'] if row else '', item.get('site') or '', names)
        drafts = self.__dict__.setdefault('learned_drafts', [])
        drafts[:] = [d for d in drafts if d['id'] != str(suggestion_id)][-20:]
        drafts.append({'id': str(suggestion_id), 'task': task, 'item': learned_skills.scrub(item, names), 'names': names, 'tries': 0})
        return 'kept: after a check it becomes a skill for later tasks on this site or workflow'

    def learned_failed(self, suggestion_id):
        """A run on this to-do got stuck: the learned skills it touched count it (RETIRE in a row turn one off)."""
        try:
            self.learned_settle(suggestion_id, False)
        except Exception as error:  # noqa: BLE001 - a blocker is saved whatever happens here
            LOG.error('learned skill settle error=%s', type(error).__name__)

    def learned_step(self):
        """Start the check of what runs handed in, when there is some and the budget allows; it runs in its own thread.
        True when started."""
        running = getattr(self, 'learned_thread', None)
        if (running and running.is_alive()) or not self.__dict__.get('learned_drafts'):
            return False
        if self.background_pause(job='learned_skills') or not self.background_spaced():
            return False
        self.background_started()
        self.learned_thread = threading.Thread(target=self.learned_run, daemon=True, name='learned-skills')
        self.learned_thread.start()
        return True

    def learned_run(self, ask=None):
        """One check turn over the oldest drafts: a model turn of its own, no tools, that never saw the runs
        (learned_skills.check_page), then what it kept becomes a skill, unless one of the owner's covers it."""
        ask = ask or getattr(self, 'learned_model', None)  # tests and the sandbox: (page) -> reply
        pending = self.__dict__.get('learned_drafts') or []
        drafts = pending[:learned_skills.BATCH]
        if not drafts:
            return {}
        try:
            page = learned_skills.check_page(drafts)
            if ask:
                reply = ask(page)
            else:
                model = background_model(self.config)
                reply = help_chat.openclaw_model_run(self.config, page, '/'.join(model) if model else None, timeout=learned_skills.TIMEOUT)
        except help_chat.Unavailable:
            return {'error': 'unavailable'}  # the turn never ran: no try spent
        except Exception as error:  # noqa: BLE001 - an unreadable turn is a try without an answer
            LOG.info('learned skills check error=%s', type(error).__name__)
            reply = None
        names = sorted({n for d in drafts for n in d['names']}, key=lambda n: -len(n[0]))
        kept, waiting, dropped = learned_skills.conclude(drafts, reply, names)
        for d in waiting:
            d['tries'] += 1
        pending[:] = [d for d in pending if d not in drafts or (d in waiting and d['tries'] < learned_skills.TRIES)]
        written, mine = [], 0
        for item in kept:
            with self.store.connect() as db:
                replaces, covered = learned_skills.place(db, item)
            if covered:  # one of the owner's own skills covers it: theirs is never changed
                mine += 1
                continue
            try:
                saved = self.skills.learn(*learned_skills.as_skill(item), replaces=replaces)
            except Exception as error:  # noqa: BLE001 - one that doesn't fit a skill's shape is left out
                LOG.info('learned skill not written error=%s', type(error).__name__)
                saved = None
            if saved:
                written.append(saved)
        LOG.info('learned skills check written=%s dropped=%s mine=%s waiting=%s', len(written), dropped, mine, len(waiting))
        return {'written': written, 'dropped': dropped, 'mine': mine, 'waiting': len(waiting)}
