"""The owner's profile actions (App.action): finding their roles, the profile run with its status, evidence and save,
and the Find my skills turn's report. Moved out of assistant.App's action as is. A mixin of assistant.App
(APP_MIXINS)."""
import datetime as dt
import json

import fleet_learnings
import learning_loop
from machine.config import LOG
from machine.prompts.profile import (import_prompt, orgs_prompt, profile_prompt, PROFILE_ROOM, roles_prompt,
                                     share_history_prompt, skills_find_prompt, voices_prompt)
from machine.store.profile import PROFILE_SESSION_PREFIX
from machine.store.review import REVIEW_TERMINAL
import team_learnings
from timeutil import now

SKILLS_SESSION_PREFIX = 'agent:main:assistant-review-skills-'  # the Find my skills turn: the browser, read-only, and its report


PROFILE_SECONDS = 900


class ProfileApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'roles_start': 'roles_start_action', 'profile_start': 'profile_start_action',
               'profile_status': 'profile_status_action', 'profile_evidence': 'profile_evidence_action',
               'save_profile': 'save_profile_action', 'skills_found': 'skills_found_action'}

    def roles_start_action(self, name, args, owner_dashboard=False):
        return self.store.roles_start(bool(args.get('again')))

    def profile_start_action(self, name, args, owner_dashboard=False):
        room = args.get('room')
        return self.store.profile_start(args.get('again') is True, room if isinstance(room, int) and not isinstance(room, bool) else None)

    def profile_status_action(self, name, args, owner_dashboard=False):
        return self.store.profile_status(args['run_id'])

    def profile_evidence_action(self, name, args, owner_dashboard=False):
        return self.store.profile_evidence(args.get('page', 1), args.get('_profile_session'))

    def save_profile_action(self, name, args, owner_dashboard=False):
        return self.store.save_profile(args.get('profile'), args.get('_profile_session'))

    def skills_found_action(self, name, args, owner_dashboard=False):
        # the Find my skills turn's report; its run is the one bound to its own session
        session = str(args.get('_skills_session') or '')
        if not session.startswith(SKILLS_SESSION_PREFIX):
            raise ValueError('Only the Find my skills turn reports skills')
        return self.skills_found({**args, 'run': session[len(SKILLS_SESSION_PREFIX):]})

    def profile_step(self, runner=None):
        """Start and follow the one profile turn `assistant profile` asked for (reviews may be off)."""
        runner = runner or self.preparation_gateway
        with self.store.connect() as db:
            # The one being followed first, then what the owner asked for, then The Machine's own
            run = db.execute("SELECT * FROM profile_runs WHERE status IN ('starting','running') ORDER BY status='running' DESC,coalesce(auto,0),started_at LIMIT 1").fetchone()
            ready = run and run['status'] == 'starting' and (not run['auto'] or self.store.first_magic_done(db))
        if not run:
            return None
        run, stamp = dict(run), dt.datetime.fromisoformat(now())
        if run['status'] == 'starting':
            # One usage check before every background turn (model_budget); The Machine's own turns (profile, voices, roles,
            # organizations) wait for the first card and start one per BACKGROUND_GAP_SECONDS. A usage limit holds all.
            if self.background_pause(owner=not run['auto'], job='profile:' + run['run_id']) or (run['auto'] and not (ready and self.background_spaced())):
                return None
        age = (stamp - dt.datetime.fromisoformat(run['started_at'])).total_seconds()
        if run['status'] == 'starting' and run['attempts'] and run['updated_at'] > (stamp - dt.timedelta(minutes=1)).isoformat():
            return None
        if run['status'] == 'starting' and run['attempts'] >= 5:
            with self.store.connect() as db:
                db.execute("UPDATE profile_runs SET status='error',error='openclaw_unavailable',finished_at=?,updated_at=? WHERE run_id=?", (now(), now(), run['run_id']))
            return 'error'
        action = 'stop' if age > PROFILE_SECONDS + 300 else 'start' if run['status'] == 'starting' else 'status'
        skills_run = run.get('kind') == 'skills'
        request = {'kind': 'skills' if skills_run else 'profile', 'job_id': run['run_id'], 'action': action}
        accounts = None
        if action == 'start' and skills_run:
            started = self.skills_find_begin(run)
            if started is None:
                return None  # the browser is busy with another task: try again on the next step
            if started is False:
                return 'ok'  # nothing to read: every account asked for is signed out
            accounts = started
        if action == 'start':
            first = self.store.profile_evidence(1, PROFILE_SESSION_PREFIX + run['run_id']) if not skills_run else None
            request['message'] = (skills_find_prompt(run['run_id'], {**json.loads(run['evidence']), 'items': accounts['items']}, self.config) if skills_run else
                                  roles_prompt(run['run_id'], first['pages']) if run.get('kind') == 'roles' else
                                  import_prompt(run['run_id']) if run.get('kind') == 'import' else
                                  orgs_prompt(run['run_id'], first['pages']) if run.get('kind') == 'orgs' else
                                  share_history_prompt(run['run_id'], first['pages'], self.share_groups()) if run.get('kind') == 'share' else
                                  voices_prompt(run['run_id'], first['counts'], first['pages']) if run.get('kind') == 'voices' else
                                  team_learnings.prompt(run['run_id'], json.loads(run['evidence'])) if run.get('kind') == 'learnings' else
                                  learning_loop.prompt(run['run_id']) if run.get('kind') == 'tune' else
                                  fleet_learnings.prompt(run['run_id']) if run.get('kind') == 'fleet_learn' else
                                  team_learnings.vote_prompt(run['run_id'], json.loads(run['evidence'])) if run.get('kind') == 'team_votes' else
                                  profile_prompt(run['run_id'], first['counts'], run.get('room') or PROFILE_ROOM))
            with self.store.connect() as db:
                db.execute('UPDATE profile_runs SET attempts=attempts+1,updated_at=? WHERE run_id=?', (now(), run['run_id']))
        result = runner(request).get('status', 'unavailable')
        with self.store.connect() as db:
            if result == 'admitted':
                if run['auto']:
                    self.background_started()
                db.execute("UPDATE profile_runs SET status='running',error=NULL,updated_at=? WHERE run_id=?", (now(), run['run_id']))
            elif result in REVIEW_TERMINAL or (action == 'stop' and age > PROFILE_SECONDS + 900):
                draft = db.execute('SELECT draft FROM profile_runs WHERE run_id=?', (run['run_id'],)).fetchone()[0]
                if run.get('kind') in ('roles', 'orgs'):  # done is done: a person left without one was unclear
                    draft = draft or (result == 'ok')
                status = 'ok' if draft else 'error'
                error = None if draft else ('no_draft' if result == 'ok' else result)
                db.execute('UPDATE profile_runs SET status=?,error=?,finished_at=?,updated_at=? WHERE run_id=?', (status, error, now(), now(), run['run_id']))
                if run.get('kind') == 'skills':
                    self.skills_find_done(run, status)
        if run.get('kind') == 'learnings':  # asks the owner only once the run is ok
            with self.store.connect() as db:
                batch = team_learnings.finish(db, run['run_id'])
            if batch:
                LOG.info('learnings ready')
                self.learnings_auto_send()  # sent at once when the owner chose Send automatically
        if run.get('kind') == 'tune':  # applies only once the run is ok; each change can be undone
            changed = self.store.apply_tune(run['run_id'])
            if changed:
                LOG.info('learning pass changes=%s', changed)
        if run.get('kind') == 'fleet_learn' and getattr(self, 'fleet', None):  # kept only once the run is ok, each one checked
            with self.store.connect() as db:
                kept = fleet_learnings.finish(db, run['run_id'], team_learnings.known_names(db, self.config), log=self.fleet.log)
            if kept:
                LOG.info('team learnings kept=%s', len(kept))
        if run.get('kind') == 'team_votes':  # sends only the votes, once the run is ok
            self.team_votes_send(run['run_id'])
        if run.get('kind') == 'voices':  # applies only once the run is ok
            written = self.store.apply_voice_study(run['run_id'])
            if written:
                LOG.info('voice study channels=%s', written)
        if run.get('auto') and run.get('kind') == 'profile':  # saves only once the run is ok
            self.first_profile_save(run['run_id'])
        return result
