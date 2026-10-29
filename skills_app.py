"""Skills, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

The skill actions (Settings, Skills: install, import, share, decide; and from the agent, skill_propose and
skill_import_report), the skills kept here, and the end of a Find my skills turn. SKILL_ACTIONS in assistant.py stays
the reviewed list of the owner's skill actions. What still uses helpers defined in assistant.py (the Find my skills
browser turn, skills_read, the notes prompt) stays there for now."""
import json


class SkillsApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = dict.fromkeys((
        'skill_decide',
        'skill_delete',
        'skill_example',
        'skill_get',
        'skill_hint_dismiss',
        'skill_hub_get',
        'skill_hub_install',
        'skill_hub_search',
        'skill_import_find',
        'skill_import_install',
        'skill_import_paste',
        'skill_import_read',
        'skill_import_report',  # from the Find my skills turn only
        'skill_import_run',
        'skill_import_signin',
        'skill_import_status',
        'skill_import_upload',
        'skill_installed',
        'skill_installed_get',
        'skill_installed_toggle',
        'skill_propose',  # from the agent: waits for the owner's Approve
        'skill_save',
        'skill_share',
        'skill_toggle',
    ), 'skills_action')

    def skills_action(self, name, args, owner_dashboard):
        return self.skill_action(name, args)

    def skill_action(self, name, args):
        keeper = self.skills
        if name == 'skill_propose':  # from the agent: waits for the owner's Approve
            return keeper.propose(args.get('name'), args.get('description'), args.get('body'), args.get('why') or '', args.get('update'),
                                  args.get('related'), args.get('relation'), args.get('new') is True, args.get('base'))
        if name == 'skill_save':  # id: an existing skill; body may be a whole pasted SKILL.md
            return keeper.save(str(args.get('id') or ''), args.get('name') or '', args.get('description') or '', args.get('body') or '')
        if name == 'skill_get':
            return keeper.get(str(args.get('id') or ''))
        if name == 'skill_example':
            return keeper.example(str(args.get('key') or 'customer-inquiries'))
        if name == 'skill_toggle':
            return keeper.toggle(str(args.get('id') or ''), bool(args.get('on')))
        if name == 'skill_delete':
            return keeper.delete(str(args.get('id') or ''))
        if name == 'skill_share':  # to: member ids, or none for everyone in that Fleet
            to = args.get('to')
            return keeper.share(str(args.get('id') or ''), str(args.get('fleet') or ''), to if isinstance(to, list) else None, str(args.get('note') or ''))
        if name == 'skill_decide':
            return keeper.decide(str(args.get('id') or ''), str(args.get('choice') or ''), str(args.get('reviewed') or '')[:64] or None)
        if name == 'skill_installed':  # refresh: read OpenClaw's list again now
            return keeper.installed(args.get('refresh') is True)
        if name == 'skill_installed_get':
            return keeper.installed_get(str(args.get('name') or ''))
        if name == 'skill_installed_toggle':
            return keeper.installed_toggle(str(args.get('name') or ''), args.get('on') is True)
        if name == 'skill_hub_search':
            return keeper.hub_search(str(args.get('query') or ''))
        if name == 'skill_hub_get':
            return keeper.hub_get(str(args.get('ref') or ''))
        if name == 'skill_hub_install':  # exactly the release the owner read: its version and its SKILL.md's sha
            return keeper.hub_install(str(args.get('ref') or ''), str(args.get('version') or ''), str(args.get('sha') or ''))
        if name == 'skill_hint_dismiss':
            return keeper.hint_dismiss(str(args.get('id') or ''))
        if name == 'skill_import_find':  # with token and sites: look again in those accounts, after signing in
            return keeper.import_find(str(args.get('token') or '') or None, args.get('sites'))
        if name == 'skill_import_signin':
            return self.skills_signin(str(args.get('site') or ''))
        if name == 'skill_import_upload':  # from: claude or chatgpt; data: {name, zip} or {name, files: [{path, data}]}, base64
            return keeper.import_upload(str(args.get('from') or ''), args.get('data'))
        if name == 'skill_import_paste':
            return keeper.import_paste(str(args.get('from') or ''), args.get('text'))
        if name == 'skill_import_status':
            return keeper.import_status(str(args.get('token') or ''))
        if name == 'skill_import_read':
            return keeper.import_read(str(args.get('token') or ''), str(args.get('key') or ''))
        if name == 'skill_import_run':
            return keeper.import_run(str(args.get('token') or ''), args.get('keys'), args.get('replace') is True)
        if name == 'skill_import_install':  # exactly what the owner read: its files' hash
            return keeper.import_install(str(args.get('token') or ''), str(args.get('key') or ''), str(args.get('sha') or ''))
        if name == 'skill_import_report':  # from the Find my skills turn only
            return self.skills_found(args)
        raise ValueError('Unknown skill action')

    def own_skills(self):
        """The owner's own skills (made here, approved or imported), which notes may go into; never a teammate's."""
        return [s for s in self.skills_on_hand() if s['origin'] != 'shared']

    def skills_on_hand(self):
        """Every skill The Machine keeps here (on or off), a teammate's included: what a new one is checked against."""
        with self.store.connect() as db:
            if not db.execute("SELECT 1 FROM sqlite_master WHERE name='skills'").fetchone():
                return []
            return [dict(r) for r in db.execute("SELECT id,name,slug,description,origin,body,sha FROM skills WHERE status IN ('on','off') ORDER BY name")]

    def skills_find_done(self, run, status):
        """The Find my skills turn ended: the list says so, and its browser lease is let go if it still holds it."""
        try:
            self.skills.importer.finished(json.loads(run['evidence'])['token'], status)
        except (ValueError, KeyError, TypeError):
            pass
        self.skills_lease_release()
