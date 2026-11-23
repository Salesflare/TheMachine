"""Learned skills, the App's part: a domain mixin of App (only machine/main.py composes it; docs/code-map.md).

A run's procedure on prepare (learned_check before the save, learned_saved after it), the skills a run opened and what it
says of them (learned_used, after either save), and the check turn for what runs handed in (learned_step, learned_run),
which writes what it kept as skills of origin 'learned' (skills.Skills.learn). The rules are in learned_skills.py; the
skills table is skills.py's."""
import logging
import threading

import help_chat
import learned_skills
from machine import cards
import memory_use
from models import background_model
import team_learnings

LOG = logging.getLogger('personal-assistant')


class LearnedSkillsApp:
    ACTIONS = {}  # no actions of its own: learned skills show, change and go in the Skills list (skills.py)

    def learned_used(self, suggestion_id, job_id, failed=None):
        """A run saved its result or its blocker: the skills it opened go in the log (memory_use: opened), and the learned
        ones of them it says no longer work (failed: skill_failed on its save, a slug or a list) as failed. RETIRE to-dos
        in a row turn one off. Returns the slugs turned off. Never raises: a save is never lost over it."""
        off = []
        try:
            with self.store.connect() as db:
                seen = learned_skills.opened(db, job_id)
                if not seen:
                    return off
                learned = {r['slug']: dict(r) for r in db.execute("SELECT id,slug,updated_at FROM skills WHERE origin='learned' AND status='on'")}
                said = {str(x).strip() for x in (failed if isinstance(failed, list) else [failed]) if x} & set(seen) & set(learned)
                had = {tuple(r) for r in db.execute("SELECT row_id,how FROM memory_use WHERE purpose='run' AND kind='skill' AND run_id=? AND suggestion_id=?", (str(job_id), str(suggestion_id)))}
            rows = [(slug, 'failed' if slug in said else 'opened') for slug in seen]
            memory_use.record(self.store, 'run', [['skill', slug, how, None, 0, 0] for slug, how in rows if (slug, how) not in had],
                              job_id, suggestion_id)
            for slug in said:
                with self.store.connect() as db:
                    n = learned_skills.failed_in_a_row(db, slug, learned[slug]['updated_at'])
                if n >= learned_skills.RETIRE and self.skills.retire(learned[slug]['id'], n):
                    off.append(slug)
        except Exception as error:  # noqa: BLE001 - a result or a blocker is saved whatever happens here
            LOG.error('learned skill use error=%s', type(error).__name__)
        return off

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
        """After the save: the procedure of a run that got its task done, with personal details out, waits for the
        check (learned_drafts). One that ends on a question to the owner isn't there yet. Returns what the run is told,
        or None."""
        if not item or (outcome or {}).get('state') not in learned_skills.SUCCESS:
            return None
        with self.store.connect() as db:
            row = db.execute('SELECT * FROM suggestions WHERE id=?', (str(suggestion_id),)).fetchone()
            if row and cards.result_ask({**dict(row), 'outcome': outcome}, db):
                return 'not kept: the task still waits for the owner\'s answer; give it again when it is done'
            names = self.learned_names(db, suggestion_id)
            task = learned_skills.scrub_text(row['title'] if row else '', item.get('site') or '', names)
            learned_skills.keep(db, suggestion_id, task, learned_skills.scrub(item, names))
        return 'kept: after a check it becomes a skill for later tasks on this site or workflow'

    def learned_names(self, db, suggestion_id):
        return sorted(set(team_learnings.known_names(db, self.config)) | set(learned_skills.people_on(db, suggestion_id)), key=lambda n: -len(n[0]))

    def learned_step(self):
        """Start the check of what runs handed in, when there is some and the budget allows; it runs in its own thread.
        True when started."""
        running = getattr(self, 'learned_thread', None)
        if running and running.is_alive():
            return False
        with self.store.connect() as db:
            if not learned_skills.waiting(db):
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
        with self.store.connect() as db:
            drafts = learned_skills.claim(db)
            for d in drafts:
                d['names'] = self.learned_names(db, d['id'])  # who is known now, not when the run handed it in
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
            with self.store.connect() as db:
                for d in drafts:
                    learned_skills.back(db, d, spent=False)  # the turn never ran: no try spent
            return {'error': 'unavailable'}
        except Exception as error:  # noqa: BLE001 - an unreadable turn is a try without an answer
            LOG.info('learned skills check error=%s', type(error).__name__)
            reply = None
        written, mine, waiting, dropped = [], 0, 0, 0
        for d in drafts:
            kept, unanswered, _ = learned_skills.conclude([d], reply, d['names'])
            with self.store.connect() as db:
                if unanswered:
                    waiting += 1
                    learned_skills.back(db, d)
                    continue
                replaces, covered = learned_skills.place(db, kept[0]) if kept else (None, False)
                if not kept or covered:  # nothing left of it, or one of the owner's own skills covers it: theirs is never changed
                    dropped, mine = dropped + (not kept), mine + bool(covered)
                    learned_skills.take(db, d)
                    continue
            saved = None
            try:  # written and gone from what waits in one transaction: a restart between the two can't write it twice
                saved = self.skills.learn(*learned_skills.as_skill(kept[0]), replaces=replaces, once=lambda db, d=d: learned_skills.take(db, d))
            except Exception as error:  # noqa: BLE001 - one that doesn't fit a skill's shape is left out
                LOG.info('learned skill not written error=%s', type(error).__name__)
            if saved:
                written.append(saved)
                continue
            with self.store.connect() as db:
                learned_skills.take(db, d)
        LOG.info('learned skills check written=%s dropped=%s mine=%s waiting=%s', len(written), dropped, mine, waiting)
        return {'written': written, 'dropped': dropped, 'mine': mine, 'waiting': waiting}
