"""The owner's profile actions (App.action): finding their roles, the profile run with its status, evidence and save,
and the Find my skills turn's report. Moved out of assistant.App's action as is. A mixin of assistant.App
(APP_MIXINS)."""
import datetime as dt
import json
import re
import uuid

import fleet_learnings
import learning_loop
from machine.config import LOG, WORKSPACE
from machine.prompts.profile import (import_prompt, orgs_prompt, profile_prompt, PROFILE_ROOM, roles_prompt,
                                     share_history_prompt, skills_find_prompt, voices_prompt)
from machine.store.profile import PROFILE_SESSION_PREFIX, SHARE_HISTORY_BATCH, SHARE_HISTORY_PAGE
from machine.store.review import REVIEW_TERMINAL
import team_learnings
from timeutil import local_tz, now

SKILLS_SESSION_PREFIX = 'agent:main:assistant-review-skills-'  # the Find my skills turn: the browser, read-only, and its report


PROFILE_SECONDS = 900


# The first profile on an install without the interactive installer (hosted): tries, and the wait between them.
FIRST_PROFILE_TRIES, FIRST_PROFILE_RETRY_SECONDS = 3, 6 * 3600


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

    def owner_first_names(self):
        """The owner's first name, as the config and USER.md give it ("- Name: …", "# USER.md - About …"): for
        Learning's older why lines that name them (learning_loop.to_you)."""
        names = [str(self.config.get('owner_name') or '')]
        try:
            text = self.user_md().read_text(encoding='utf-8')[:4000]
            names += re.findall(r'(?m)^- Name: *(.+)$', text) + re.findall(r'(?m)^# USER\.md - About (.+)$', text)
        except (OSError, ValueError):
            pass
        return sorted({n.split()[0] for n in names if n.split() and re.fullmatch(r"[^\W\d_][\w'’-]*", n.split()[0]) and n.split()[0].lower() not in ('me', 'the', 'you')})

    def learning_changes_shown(self, changes):
        """Learning, Changes: an older why line that names the owner reads "You corrected …" (the stored one stays)."""
        names = self.owner_first_names()
        return [{**c, 'why': learning_loop.to_you(c.get('why'), names)} for c in changes]

    def owner_role(self):
        """The Role line of USER.md ('' when there is none): only for Help's guess at how technical the owner is."""
        try:
            found = re.search(r'(?m)^- Role: *(.+)$', self.user_md().read_text(encoding='utf-8'))
        except (OSError, ValueError):
            return ''
        return found[1].strip()[:200] if found else ''

    def user_md(self):
        import onboarding
        return onboarding.user_md_path(self.config.get('openclaw_workspace') or WORKSPACE)

    @staticmethod
    def user_md_says_how(path):
        """OpenClaw's own USER.md template has no Tone line either, yet says nothing about the owner."""
        import onboarding
        return not onboarding.user_md_is_template(path) and onboarding.says_how_you_write(path)

    def first_profile_step(self, current=None):
        """Installs set up without the interactive installer (hosted Machines) never ran `assistant profile`, so reviews
        and drafts knew neither who the owner is nor how they write. Once reviews are on and USER.md still says nothing
        about how they write, one profile turn starts by itself (and names the closest people after it). Tried a few
        times at most; `first_profile: false` in the config turns it off."""
        import onboarding
        if not (self.config.get('review_worker') or {}).get('enabled') or self.config.get('first_profile') is False:
            return None
        current = current or dt.datetime.fromisoformat(now())
        if getattr(self, '_first_profile_wait', None) and self._first_profile_wait > current:
            return None
        path = self.user_md()
        if self.user_md_says_how(path):
            return None
        with self.store.connect() as db:
            runs = db.execute("SELECT status,auto,finished_at FROM profile_runs WHERE kind='profile' ORDER BY started_at").fetchall()
        if (any(not r['auto'] or r['status'] in ('starting', 'running', 'ok') for r in runs) or len(runs) >= FIRST_PROFILE_TRIES
                or (runs and (runs[-1]['finished_at'] or '') > (current - dt.timedelta(seconds=FIRST_PROFILE_RETRY_SECONDS)).isoformat())):
            return None  # the owner ran their own, one is running or done, or tried enough
        try:
            text = path.read_text() if path.exists() else onboarding.starter_user_md(self.config)
        except OSError:
            return None
        if onboarding.user_md_is_template(path):
            text = text.rstrip() + '\n\n' + onboarding.starter_user_md(self.config)
        try:
            return self.store.profile_start(room=max(onboarding.profile_room(text), 0), auto=True)
        except ValueError:  # too few of the owner's own messages yet: look again later
            self._first_profile_wait = current + dt.timedelta(seconds=FIRST_PROFILE_RETRY_SECONDS)
            return None

    def share_history_step(self):
        """The Shared Graph's history pass, when reviews are on: Work client threads from before (as far back as the
        Machine has mail) go through the same review labels, a batch per turn, one turn at a time, until none is left.
        Stops after three turns in a row that judged nothing."""
        if not (self.config.get('review_worker') or {}).get('enabled') or not getattr(self, 'fleet', None):
            return None
        with self.store.connect() as db:
            if db.execute("SELECT 1 FROM profile_runs WHERE status IN ('starting','running') LIMIT 1").fetchone():
                return None  # one turn at a time
            runs = db.execute("SELECT status,error,finished_at FROM profile_runs WHERE kind='share' ORDER BY started_at DESC LIMIT 3").fetchall()
        if len(runs) == 3 and all(r['status'] == 'error' for r in runs):
            return None
        if runs and runs[0]['finished_at'] and runs[0]['finished_at'] > (dt.datetime.fromisoformat(now()) - dt.timedelta(minutes=10)).isoformat():
            return None
        threads = self.fleet.graph_unjudged(SHARE_HISTORY_BATCH)
        if not threads:
            return None
        run_id, started = uuid.uuid4().hex, now()
        with self.store.connect() as db:
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind,auto) VALUES(?,'starting',?,?,?,'share',1)",
                       (run_id, started, started, json.dumps({'threads': threads, 'page_size': SHARE_HISTORY_PAGE})))
        return {'run_id': run_id, 'threads': len(threads)}

    def orgs_backfill_step(self):
        """Once per install, when reviews are on: one organizations turn over the people already in the graph, from
        the signals already stored. Later people get theirs from reviews. Retried when OpenClaw couldn't start it."""
        if not (self.config.get('review_worker') or {}).get('enabled'):
            return None
        with self.store.connect() as db:
            if db.execute("SELECT 1 FROM profile_runs WHERE status IN ('starting','running') LIMIT 1").fetchone():
                return None  # one turn at a time: the owner's own profile or roles first
            runs = db.execute("SELECT status,error FROM profile_runs WHERE kind='orgs'").fetchall()
            if not db.execute("SELECT 1 FROM graph_state").fetchone():
                return None  # no graph yet
        if any(r['status'] == 'ok' or r['error'] != 'openclaw_unavailable' for r in runs) or len(runs) >= 3:
            return None
        return self.store.orgs_start(auto=True)

    def first_profile_save(self, run_id):
        """The first profile's draft goes into USER.md as its own section (marked, so the owner can edit or delete
        it), never over anything that already says how the owner writes."""
        import onboarding
        with self.store.connect() as db:
            row = db.execute("SELECT draft FROM profile_runs WHERE run_id=? AND status='ok'", (run_id,)).fetchone()
        path = self.user_md()
        if not row or not row['draft'] or self.user_md_says_how(path):
            return False
        text = path.read_text() if path.exists() else onboarding.starter_user_md(self.config)
        if onboarding.user_md_is_template(path):
            text = text.rstrip() + '\n\n' + onboarding.starter_user_md(self.config)
        merged, _ = onboarding.fit_profile(text, json.loads(row['draft']), dt.datetime.now(local_tz()).date().isoformat())
        if not merged:
            return False
        path.parent.mkdir(parents=True, exist_ok=True)
        onboarding.write_private(path, merged)
        LOG.info('first profile saved to USER.md chars=%s', len(merged))
        return True
