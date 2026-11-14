"""Skills, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

The skill actions (Settings, Skills: install, import, share, decide; and from the agent, skill_propose and
skill_import_report), the skills kept here, and the end of a Find my skills turn. SKILL_ACTIONS in assistant.py stays
the reviewed list of the owner's skill actions. The Find my skills browser turn, skills_read and the notes prompt
are here too."""
import concurrent.futures
import datetime as dt
import json
import re
import secrets
import subprocess
import sys
import time
import uuid

import browser_login
import browser_viewer
from machine.browser import browser_lease_script, browser_link
from machine.app.card_actions import owner_turn
from machine.config import LOG
from machine.prompts.profile import SKILLS_LEASE, SKILLS_PAGES, SKILLS_READ, SKILLS_SIGNIN, SKILLS_SITES
from machine.store.decisions import skill_update_after
from machine.store.voices import sentences
import recurring
import skills as skills_module
import skills
from timeutil import now
from machine.owner_error import OwnerError


SKILL_NOTES_MIN = 5   # notes about one kind of task before they're offered as a skill


SKILL_REGROW = 3      # after Not now, offered again only once this many more notes joined them


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

    def skill_job_task(self, job):
        """The to-do a preparation run proposes a skill for (skills-propose --job): only its own running preparation."""
        job = str(job or '')
        if not job:
            return None
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', job):
            raise ValueError('Give the job_id of this preparation')
        with self.store.connect() as db:
            run = db.execute("SELECT suggestion_id FROM preparations WHERE job_id=? AND status IN ('queued','starting','running','blocked')",
                             (job,)).fetchone()
        if not run:
            raise OwnerError('A skill is proposed for a to-do only from its running preparation')
        return run['suggestion_id']

    def skill_task_done(self, task, skill_id):
        """The owner created the skill their to-do asked for: that to-do is done."""
        with self.store.connect() as db:
            row = db.execute('SELECT status FROM suggestions WHERE id=?', (task,)).fetchone()
        if not row or row['status'] != 'prepared':
            return
        try:
            self.store.decide(task, 'complete', '', 'skill-created:' + skill_id, 'dashboard')
        except ValueError:
            pass  # closed meanwhile: nothing left to finish

    def skill_action(self, name, args):
        keeper = self.skills
        if name == 'skill_propose':  # from the agent: waits for the owner's Approve
            task = self.skill_job_task(args.get('job_id'))
            asked = False
            if task and args.get('asked') is True:  # the owner asked for a skill in the message that started this run
                with self.store.connect() as db:
                    if not owner_turn(db, task, str(args.get('job_id'))):
                        raise ValueError('--asked is only for a run started by the owner’s own message asking for this skill; leave it out')
                asked = True
            if task and not args.get('update') and not asked:
                with self.store.connect() as db:
                    kept = (recurring.method_series(db, task) or {'method': None})['method']
                if kept:  # a repeating to-do keeps its own way of doing it: no Create skill for the same work as well, unless asked
                    raise ValueError('This to-do repeats and keeps its own way of doing it, which the next one follows: give the '
                                     'steps as method on prepare instead of proposing a skill. Only when the owner’s message asks '
                                     'for a skill, propose it with --asked')
            return keeper.propose(args.get('name'), args.get('description'), args.get('body'), args.get('why') or '', args.get('update'),
                                  args.get('related'), args.get('relation'), args.get('new') is True, args.get('base'),
                                  task=task, asked=asked)
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
            skill_id, choice = str(args.get('id') or ''), str(args.get('choice') or '')
            with self.store.connect() as db:
                task = skills_module.task_of(db, skill_id)
            view = keeper.decide(skill_id, choice, str(args.get('reviewed') or '')[:64] or None)
            if task and choice == 'approve':
                self.skill_task_done(task, skill_id)
            return view
        if name == 'skill_installed':  # refresh: read OpenClaw's list again now; else never a wait on OpenClaw (loading)
            return keeper.installed(args.get('refresh') is True, wait=False)
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

    def skills_read(self, sites):
        """The owner's own skills on claude.ai and chatgpt.com, read in the Machine's browser: a tab straight on each
        site's skills page (SKILLS_PAGES), SKILLS_READ run there, the tab closed again. {'chatgpt': {'state': 'ok' |
        'signed_out' | 'unavailable', 'skills': [...], 'where': <page>, 'detail': …}}. Read-only; nothing is clicked."""
        try:
            base = browser_login.endpoints(self.config)[0]
        except (IndexError, TypeError):
            return {s: {'state': 'unavailable', 'where': SKILLS_PAGES[s], 'detail': 'the Machine’s browser isn’t running'} for s in sites}
        cdp = browser_login.browser_cdp

        def read(site):
            seen = {'where': SKILLS_PAGES[site]}
            try:
                tab = cdp.open_tab(base, SKILLS_PAGES[site])
            except (cdp.CdpError, OSError):
                return {**seen, 'state': 'unavailable', 'detail': 'the Machine’s browser didn’t open it'}
            try:
                for _ in range(25):  # up to ~25 seconds for the page to load its own origin
                    time.sleep(1)
                    try:
                        if cdp.evaluate(base, tab, "() => location.hostname + ' ' + document.readyState", timeout_ms=3000) == SKILLS_SITES[site] + ' complete':
                            break
                    except (cdp.CdpError, OSError):
                        pass
                got = cdp.evaluate(base, tab, SKILLS_READ[site], timeout_ms=120000)
            except (cdp.CdpError, OSError):
                return {**seen, 'state': 'unavailable', 'detail': 'the page didn’t answer'}
            finally:
                try:
                    cdp.close_tab(base, tab)
                except (cdp.CdpError, OSError):
                    pass
            if not isinstance(got, dict) or got.get('state') not in ('ok', 'signed_out', 'unavailable'):
                return {**seen, 'state': 'unavailable', 'detail': 'the page didn’t answer'}
            skills = [f for f in got.get('skills') or [] if isinstance(f, dict)][:60]
            out = {**seen, 'state': got['state'], 'skills': skills}
            if got['state'] == 'ok' and not skills:
                out['detail'] = (f"{got.get('failed')} couldn’t be downloaded" if got.get('failed') else 'none you made or uploaded yourself')
            elif got.get('detail'):
                out['detail'] = str(got['detail'])[:120]
            return out
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            return dict(zip(sites, pool.map(read, sites)))

    def skills_find_begin(self, run):
        """Before the Find my skills turn: the service takes the browser lease, reads the owner's own skills from the
        accounts asked for (skills_read) and adds them to the list. Returns {'accounts': states, 'items': the list to
        judge}, None when the browser is busy, or False when there is nothing to judge (the run is then done)."""
        evidence = json.loads(run['evidence'])
        try:
            claimed = subprocess.run([sys.executable, str(browser_lease_script(self.config)), 'claim', '--owner', SKILLS_LEASE,
                                      '--minutes', '20'], capture_output=True, timeout=60).returncode
        except (OSError, subprocess.TimeoutExpired):
            claimed = 0  # no lease helper: the read goes ahead as before
        if claimed == 3:
            return None
        for site in evidence.get('sites') or ():  # the sign-in tab the dashboard opened has done its job
            tab = self.__dict__.get('skills_signin_tabs', {}).pop(site, None)
            if tab:
                try:
                    browser_login.browser_cdp.close_tab(browser_login.endpoints(self.config)[0], tab)
                except (browser_login.browser_cdp.CdpError, OSError, IndexError):
                    pass
        sites = [s for s in evidence.get('sites') or SKILLS_SITES if s in SKILLS_SITES]
        try:
            read = self.skills_read(sites) if sites else {}
        finally:  # the turn after this reads no page: the browser is free again
            self.skills_lease_release()
        accounts = {s: r.get('state', 'unavailable') for s, r in read.items()}
        found = [{**f, 'from': s} for s, r in read.items() for f in r.get('skills') or []]
        importer, token, items = self.skills.importer, evidence['token'], []
        try:
            importer.accounts(token, accounts, read)
            importer.report(token, found, [], accounts)  # every account read is done now
            scan = importer.scan(token)
            items = importer.brief(i for i in scan['items'].values() if not evidence.get('more') or i['public']['from'] in sites)
            LOG.info('skills read from accounts %s', ' '.join(f"{s}={r.get('state')}:{len(r.get('skills') or [])}" for s, r in read.items()))
        except (KeyError, AttributeError, ValueError):
            pass
        if not any(not i['blocked'] and not i['here'] for i in items):  # nothing to judge: no turn
            with self.store.connect() as db:
                db.execute("UPDATE profile_runs SET status='ok',draft=?,finished_at=?,updated_at=? WHERE run_id=?",
                           (json.dumps({'reported': False}), now(), now(), run['run_id']))
            self.skills_find_done(run, 'ok')
            return False
        return {'accounts': accounts, 'items': items[:150]}

    def apply_skill_clusters(self):
        """The owner tapped Create skill (or Update <skill>, after its before and after): write the skill with the instructions, and move the notes into it.
        They stay in the database, shown with the skill, and leave the list every task gets."""
        if not getattr(self, 'skills', None):
            return 0
        with self.store.connect() as db:
            rows = [dict(r) for r in db.execute("SELECT * FROM skill_clusters WHERE status='accepting'")]
        for offered in rows:
            try:
                with self.store.connect() as db:
                    db.execute('BEGIN IMMEDIATE')
                    # Dashboard and the worker can both pick the same offer; reconcile under the write lock.
                    c = db.execute("SELECT * FROM skill_clusters WHERE id=? AND status='accepting'", (offered['id'],)).fetchone()
                    if not c:
                        continue
                    if c['target_id']:
                        row = db.execute("SELECT * FROM skills WHERE id=? AND status IN ('on','off') AND origin!='shared'", (c['target_id'],)).fetchone()
                        if not row:
                            raise OwnerError('That skill is gone')
                        if c['reviewed_sha'] and row['sha'] != c['reviewed_sha'] or c['base_sha'] and row['sha'] != c['base_sha']:
                            raise OwnerError('That skill changed after its before and after were shown')
                        after = c['body'] if c['base_sha'] else skill_update_after(row['body'], c['body'])
                        skill_id = self.skills.save(row['id'], row['name'], row['description'], after, _db=db)
                    else:
                        skill_id = self.skills.save(None, c['name'], c['description'], c['body'], _db=db)
                    ids = json.loads(c['fact_ids'])
                    moved = db.execute('UPDATE facts SET removed_at=?,merged_into=? WHERE removed_at IS NULL AND id IN (' + ','.join('?' for _ in ids) + ')',
                                       (now(), 'skill:' + skill_id, *ids)).rowcount
                    db.execute("INSERT INTO rule_changes(at,kind,text,ref) VALUES(?,'condense',?,?)",
                               (now(), f'Moved {moved} notes into the skill {c["target_name"] or c["name"]}', 'skill:' + skill_id))
                    db.execute("UPDATE skill_clusters SET status='done',skill_id=?,updated_at=? WHERE id=?", (skill_id, now(), c['id']))
            except (ValueError, OSError) as error:
                LOG.error('skill from notes error=%s', type(error).__name__)
                with self.store.connect() as db:
                    db.execute("UPDATE skill_clusters SET status='failed',updated_at=? WHERE id=? AND status='accepting'", (now(), offered['id']))
                    db.execute("UPDATE suggestions SET status='pending' WHERE id=? AND EXISTS(SELECT 1 FROM skill_clusters WHERE id=? AND status='failed')", (offered['suggestion_id'], offered['id']))
        # Files are derived from the committed skills, never a reason to replay the database operation.
        self.skills.sync()
        return len(rows)

    def propose_skill_from_notes(self, name, description, body, replaces, into=None, related=None, relation=None, new=False, base=None):
        """Notes that are all about one kind of task become a suggestion card. It is checked against the skills here
        first (the review judges that by meaning, from their names and descriptions): when one of the owner's own already
        does the same job (into), the card offers Update <skill>: the review gets its instructions first (rewrite_needed)
        and sends the whole skill rewritten as one with the notes merged in (base names that version); when one is related but a
        separate job (related, e.g. the other direction of an exchange), the card says how in one line (relation) and
        still offers the new skill. Nothing changes until they tap Create skill (or Update, after its before and after);
        Not now isn't asked again until the same notes have grown by SKILL_REGROW."""
        if not getattr(self, 'skills', None):
            raise OwnerError('Skills are not set up here')
        name, description, body = skills.validate(name, description, body)
        target, linked, relation = skills.check_against(self.skills_on_hand(), into, related, relation, new)
        if target:  # the whole skill rewritten as one, on the version the review was shown
            asked = skills.rewrite_needed(target, base)
            if asked:
                return asked
            skills.check_rewrite(target['body'], body)
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            notes = self.store.replaced_facts(db, replaces)
            if not SKILL_NOTES_MIN <= len(notes) <= 20:
                raise OwnerError(f'A skill takes {SKILL_NOTES_MIN} to 20 current notes (replaces=[their ids])')
            ids = {n['id'] for n in notes}
            title = sentences(f'Update {target["name"]} with {len(notes)} notes' if target else f'Turn {len(notes)} notes into a skill: {name}', 90)
            if target:
                text = (sentences(description, 250) + f"\n\nThese {len(notes)} notes fit {target['name']}. Update shows the before and after first; "
                        'only that skill changes. Not now keeps the notes as they are.')
            else:
                text = (sentences(description, 250) + (f"\n\nRelated to {linked['name']}: {relation}" if linked else '')
                        + f"\n\nI can keep these {len(notes)} notes together in a skill. Read the full instructions and notes before deciding. "
                        'Create skill makes it, on, under Skills. Not now keeps them as they are.')
            fields = {'name': name, 'description': description, 'body': body, 'target_id': target and target['id'], 'target_name': target and target['name'],
                      'base_sha': target and target['sha'],
                      'related_id': linked and linked['id'], 'related_name': linked and linked['name'], 'relation': relation if linked else None}
            for old in db.execute("SELECT c.id,c.fact_ids,c.status,c.checked,c.suggestion_id,c.base_sha,k.sha target_sha FROM skill_clusters c "
                                  "LEFT JOIN skills k ON k.id=c.target_id WHERE c.status IN ('pending','accepting','declined')").fetchall():
                before = set(json.loads(old['fact_ids']))
                if len(ids & before) * 2 >= len(before):
                    if old['status'] == 'pending' and (not old['checked'] or not old['base_sha'] and old['target_sha'] or old['base_sha'] and old['base_sha'] != old['target_sha']):
                        # Offered before skills were checked first, as an addition, or on a version of the skill changed since:
                        # the same card, brought up to date.
                        db.execute('UPDATE skill_clusters SET fact_ids=?,' + ','.join(k + '=?' for k in fields) + ',checked=1,updated_at=? WHERE id=?',
                                   (json.dumps(sorted(ids)), *fields.values(), now(), old['id']))
                        db.execute("UPDATE suggestions SET title=?,body=? WHERE id=? AND status='pending'", (title, text[:700], old['suggestion_id']))
                        db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (old['suggestion_id'],))
                        return {'id': old['id'], 'suggestion_id': old['suggestion_id'], 'updated': True}
                    if old['status'] != 'declined':
                        return {'id': old['id'], 'duplicate': True}
                    if len(ids) < len(before) + SKILL_REGROW:
                        raise OwnerError(f'The owner said Not now to these notes; suggest it again once {SKILL_REGROW} more have joined them')
            cards = [n['suggestion_id'] for n in notes if n['suggestion_id']]
            events = list(dict.fromkeys(i for r in db.execute('SELECT event_ids FROM suggestions WHERE id IN (' + ','.join('?' for _ in cards) + ')', cards)
                                        for i in json.loads(r['event_ids'] or '[]')))[:20] if cards else []
            if not events:
                raise OwnerError('These notes have no cards behind them to show as evidence')
            cluster = 'sc_' + secrets.token_hex(6)
            card = self.store.suggest('skill-notes:' + cluster, title, text[:700], events, _db=db)
            db.execute('INSERT INTO skill_clusters(id,fact_ids,' + ','.join(fields) + ",suggestion_id,status,checked,created_at,updated_at) "
                       'VALUES(?,?,' + ','.join('?' for _ in fields) + ",?,'pending',1,?,?)",
                       (cluster, json.dumps(sorted(ids)), *fields.values(), card['id'], now(), now()))
        return {'id': cluster, 'suggestion_id': card['id']}

    def skills_from_notes_prompt(self):
        """The condense pass's line on turning notes into a skill: the skills here first, by name and what each is for,
        so the review judges by meaning whether one already does that job (update it) or sits next to it (related)."""
        try:
            on_hand = self.skills_on_hand()
        except Exception:
            on_hand = []
        listed = '\n'.join(f"- {s['name']}: {s['description']}" + (" (a teammate's: can be related, never updated)" if s['origin'] == 'shared' else '')
                           for s in on_hand)[:4000]
        return (f"\nWhen {SKILL_NOTES_MIN} or more notes are all about one specific kind of task or scenario (not how the owner writes in general), "
                "suggest moving them into a skill: remember_fact kind=skill, name, description=<when to use it, one sentence>, "
                "text=<SKILL.md instructions that keep everything those notes say>, replaces=[their ids]. The owner decides on a card. "
                + ("First check the skills below by what each is for, judging the meaning, not shared words. When one of the owner's own "
                   "already does the same job, add skill=<its name>: you get its instructions back, then send the whole skill rewritten as "
                   "one in text, with what the notes add merged into its own sections (no heading twice, no step said twice), and base=<what "
                   "you got>; the card offers to update that skill. When one is related but a separate job (say the other direction of the "
                   "same exchange), add related=<its name> and relation=<how they relate, one short line>: still a new skill. When none "
                   "is, add new=true.\nSkills here:\n" + listed if on_hand else "They have no skills yet."))

    def skills_find_start(self, token, items, sites=None, more=False):
        """Find my skills on the service: reads the owner's own skills from claude.ai and chatgpt.com (`sites`: only
        those) in the Machine's own browser, then a turn judges which listed skills would help with this Machine's
        actual work. One at a time. `more`: looking again after the owner signed in to one."""
        with self.store.connect() as db:
            if db.execute("SELECT 1 FROM profile_runs WHERE status IN ('starting','running')").fetchone():
                return None  # another turn of this kind is on; the list still shows what is on this computer
            since = (dt.datetime.fromisoformat(now()) - dt.timedelta(days=30)).isoformat()
            cards = [r[0] for r in db.execute('SELECT title FROM suggestions WHERE created_at>? ORDER BY created_at DESC LIMIT 40', (since,))]
            run_id, started = uuid.uuid4().hex, now()
            evidence = {'token': token, 'cards': cards, 'sites': [s for s in (sites or SKILLS_SITES) if s in SKILLS_SITES], 'more': bool(more),
                        'sources': sorted({str(a.get('service') or '') for a in self.config.get('accounts', []) if a.get('service')}),
                        'skills': sorted(self.skills.mine())[:60]}
            db.execute("INSERT INTO profile_runs(run_id,status,started_at,updated_at,evidence,kind) VALUES(?,'starting',?,?,?,'skills')",
                       (run_id, started, started, json.dumps(evidence)))
        return run_id

    def skills_signin(self, site):
        """Sign in to ChatGPT or claude.ai for Find my skills: its sign-in page in front in the Machine's browser, for
        the dashboard's sign-in dialog. Nothing is typed here."""
        if site not in SKILLS_SIGNIN:
            raise OwnerError('Which account?')
        try:
            base = browser_login.endpoints(self.config)[0]
            tab = browser_login.browser_cdp.open_tab(base, SKILLS_SIGNIN[site])
        except (browser_login.browser_cdp.CdpError, OSError, IndexError):
            raise OwnerError('I couldn’t open the sign-in page in the browser') from None
        self.__dict__.setdefault('skills_signin_tabs', {})[site] = tab
        try:
            browser_viewer.focus(SKILLS_SIGNIN[site], base)
        except (ValueError, OSError):
            pass
        return {'opened': True, 'site': SKILLS_SITES[site], 'view': browser_link(self.config)}

    def skills_found(self, args):
        run_id = str(args.get('run') or '')
        with self.store.connect() as db:
            run = db.execute("SELECT evidence FROM profile_runs WHERE run_id=? AND kind='skills' AND status IN ('starting','running')", (run_id,)).fetchone()
            if not run:
                raise OwnerError('This Find my skills run is no longer active')
            db.execute('UPDATE profile_runs SET draft=?,updated_at=? WHERE run_id=?', (json.dumps({'reported': True}), now(), run_id))
        token = json.loads(run['evidence'])['token']
        return self.skills.importer.report(token, args.get('found'), args.get('recommended'), args.get('browser'))

    def skills_lease_release(self):
        try:
            subprocess.run([sys.executable, str(browser_lease_script(self.config)), 'release', '--owner', SKILLS_LEASE], capture_output=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired):
            pass
