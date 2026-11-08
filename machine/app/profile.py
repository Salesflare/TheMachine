"""The owner's profile actions (App.action): finding their roles, the profile run with its status, evidence and save,
and the Find my skills turn's report. Moved out of assistant.App's action as is. A mixin of assistant.App
(APP_MIXINS)."""

SKILLS_SESSION_PREFIX = 'agent:main:assistant-review-skills-'  # the Find my skills turn: the browser, read-only, and its report


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
