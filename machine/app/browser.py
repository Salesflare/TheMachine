"""The dashboard's browser actions (App.action): bringing the browser or a task's page to the front, and signing in to
sites through the encrypted login store (browser_login.py), where what the owner types never reaches a log, the model
or an error message. Moved out of assistant.App's action as is. A mixin of assistant.App (APP_MIXINS)."""
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import time
import urllib.parse

import browser_login
import browser_viewer
from machine.browser import (browser_lease_script, browser_link, browser_wait, preparation_steps, run_tab,
                             same_site, signin_address, signin_handoff, signin_kind, signin_name, SIGNIN_WATCH,
                             site_language, task_page)
from machine.config import BROWSER_LEASE, LOG
import mail_attachments
import next_actions
import security_levels
from timeutil import now
from machine import todo_states
from machine.owner_error import OwnerError


class BrowserApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'browser_focus': 'browser_focus_action', 'browser_show': 'browser_show_action',
               'browser_login_open': 'browser_login_action', 'browser_login_pages': 'browser_login_action',
               'browser_login_fill': 'browser_login_action', 'browser_login_choose': 'browser_login_action',
               'browser_login_check': 'browser_login_action', 'browser_logins': 'browser_login_action',
               'browser_login_forget': 'browser_login_action'}

    def browser_focus_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise OwnerError('Only the owner brings the browser to the front, from the dashboard')
        page = args.get('page') if isinstance(args.get('page'), str) else None
        if isinstance(args.get('suggestion_id'), str):  # a task's own tab, never another task's
            page = self.signin_page(args['suggestion_id']) or self.preparing_page(args['suggestion_id'])
            if not page:
                return {'shown': False, 'unknown': True}
            return self.task_front(page)
        shown = browser_viewer.focus(page, self.config.get('browser_cdp_url') or browser_viewer.CDP_URL)
        return {'shown': shown is not None}

    def browser_show_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise OwnerError('Only the owner opens a task’s page in the browser, from the dashboard')
        if not isinstance(args.get('suggestion_id'), str):
            raise OwnerError('Which task?')
        return self.browser_show(args['suggestion_id'])

    def browser_login_action(self, name, args, owner_dashboard=False):
        # A separate path: what the owner types goes into the page and, when asked, the encrypted store, never
        # into a log, the model or an error message (see browser_login.py).
        if not owner_dashboard:
            raise OwnerError('Only the owner signs in to sites, from the dashboard')
        logins = browser_login.LoginStore(Path(self.config['database']).expanduser().parent)
        if name == 'browser_login_open':
            if not isinstance(args.get('suggestion_id'), str):
                raise OwnerError('Which task?')
            return self.signin_open(args['suggestion_id'])
        if name == 'browser_login_check':
            # The owner closed the browser (its pane, the dialog's view): look now rather than at the next round, so a
            # task whose sign-in is done carries on at once. Read-only, the same look as watch_sign_ins.
            return {'resumed': self.watch_sign_ins(now=True)}
        if name == 'browser_login_pages' and isinstance(args.get('watch'), str):
            # the dialog after a sign-in it sent waits on the owner elsewhere (approving it in the site's app)
            seen = browser_login.watch(self.config, args['watch'])
            if seen['state'] == 'done' and isinstance(args.get('host'), str):
                task = args.get('suggestion_id') if isinstance(args.get('suggestion_id'), str) else None
                seen['resumed'] = self.resume_signed_in(host=args['host'], suggestion_id=task)
            return seen
        if name == 'browser_login_pages':
            account = args.get('account') if isinstance(args.get('account'), str) else None
            found = browser_login.pages(self.config, logins, account)
            # No form, but a bot wall in front of the site: the dialog says so (and, hosted, how to get past it)
            walls = [] if found else browser_login.walls(self.config, account)
            if isinstance(args.get('suggestion_id'), str):
                # For a task, only the sign-in on the site its own run left off at; unknown: none, never a guess.
                page = self.signin_page(args['suggestion_id'])
                found = [p for p in found if page and same_site(p['host'], page)]
                walls = [w for w in walls if page and same_site(w['host'], page)]
                return {'pages': found, 'walls': walls, 'task_site': browser_login.site(urllib.parse.urlsplit(page).hostname) if page else None}
            return {'pages': found, 'walls': walls}
        if name == 'browser_logins':
            store = getattr(self, 'store', None)
            if store is None:
                return {'logins': logins.list()}
            with store.connect() as db:
                offer = security_levels.save_logins(db)
            return {'logins': logins.list(), 'save': offer}
        if name == 'browser_login_forget':
            if args.get('all') is True:  # Settings, Security: Forget all saved sign-ins
                return {'forgotten': sum(1 for x in logins.list() if logins.forget(x['site']))}
            return {'forgotten': logins.forget(args.get('site'))}
        host = args.get('host') if isinstance(args.get('host'), str) else ''
        if name == 'browser_login_choose':  # the page's own "use another method" or "resend": a click, nothing typed
            return browser_login.choose(self.config, args.get('page'), host, args.get('option'))
        username, password = (v if isinstance(v, str) else None for v in (args.get('username'), args.get('password')))
        if args.get('use_saved') is True:
            saved = logins.get(host)
            if not saved:
                raise OwnerError('Nothing is saved for ' + browser_login.site(host))
            username, password = username or saved.get('username'), saved.get('password')
        code = args.get('code') if isinstance(args.get('code'), str) else None
        done = browser_login.fill(self.config, args.get('page'), host, username, password, code)
        may_save = True
        if getattr(self, 'store', None) is not None:
            with self.store.connect() as db:
                may_save = security_levels.save_logins(db)  # Careful: Save for next time isn't offered
        if may_save and args.get('save') is True and args.get('use_saved') is not True and done['result'] != 'still_here' and (username or password):
            logins.save(host, username, password)
        if done['result'] == 'done':  # no sign-in form left: the task that waited on it carries on
            task = args.get('suggestion_id') if isinstance(args.get('suggestion_id'), str) else None
            done['resumed'] = self.resume_signed_in(host=host, suggestion_id=task)
        return done

    def peek_target(self, job_id):
        """(DevTools address, target ID) of the tab a running preparation works in (run_tab: also between its browser
        steps, so its card and chat keep the picture until it is done with the browser), in the browser this install's
        DevTools address points at (loopback only); None when it uses another browser or none."""
        with self.store.connect() as db:
            tab = run_tab(db, job_id)
        base = (browser_login.endpoints(self.config) or [None])[0]
        if not tab or not base or urllib.parse.urlsplit(base).port != tab[1]:
            return None
        return base, tab[0]

    def browser_now(self):
        """What this Machine's own browser is doing, for the note in its viewer and its Stop (in the viewer and the
        dashboard's Browser pane): the running tasks that use it (to-do ID, title and latest step), the one on the tab
        in front first, and the ones waiting there for the owner to sign in (title and site). Nothing else."""
        with self.store.connect() as db:
            rows = db.execute("SELECT p.job_id,p.session_job_id,p.suggestion_id,p.status,p.reason,s.title FROM preparations p JOIN suggestions s ON s.id=p.suggestion_id "
                              "WHERE p.status IN ('starting','running','blocked') ORDER BY p.updated_at DESC LIMIT 20").fetchall()
            waits = {r['job_id']: browser_wait(db, r['job_id'], r['status'], reason=r['reason']) for r in rows if r['status'] == 'blocked'}
            try:
                used = {r['job_id'] for r in rows if r['status'] != 'blocked' and db.execute(
                    "SELECT 1 FROM preparation_calls WHERE job_id=? AND tool='browser' LIMIT 1", (r['job_id'],)).fetchone()}
            except sqlite3.OperationalError:
                used = set()
            tabs = {j: run_tab(db, j) for j in used} if len(used) > 1 else {}
        front = self.front_tab(tabs) if tabs else None
        working, waiting = [], []
        for r in rows:
            title = ' '.join(str(r['title'] or '').split())[:120]
            if r['status'] == 'blocked':
                wait = waits.get(r['job_id'])
                if wait and wait['sign_in']:
                    waiting.append({'title': title, 'site': signin_name(r['reason'], wait['page'])})
            elif r['job_id'] in used:  # a run that has used the browser counts until it ends, so the note doesn't flicker
                with self.store.connect() as db:
                    steps = preparation_steps(db, r['job_id'], 1)
                item = {'id': r['suggestion_id'], 'title': title, 'step': steps[-1]['title'] if steps else None}
                working.insert(0, item) if front and front == tabs.get(r['job_id']) else working.append(item)
        return {'working': working[:3], 'waiting': waiting[:3]}

    def front_tab(self, tabs):
        """Which of these runs' tabs (job ID: (target ID, port)) the browser shows now: the one whose page is visible,
        read over DevTools without bringing anything to the front. None when none is, or the browser can't say."""
        base = (browser_login.endpoints(self.config) or [None])[0]
        port = urllib.parse.urlsplit(base).port if base else None
        for tab in dict.fromkeys(t for t in tabs.values() if t and t[1] == port):
            try:
                with browser_login.browser_cdp.Session(base, tab[0], timeout=2) as session:
                    if session.call('Runtime.evaluate', {'expression': 'document.visibilityState', 'returnByValue': True})['result'].get('value') == 'visible':
                        return tab
            except (browser_login.browser_cdp.CdpError, OSError, KeyError, TypeError, AttributeError, ValueError):
                continue
        return None

    def seal_attachments(self, every=60):
        """Email attachments that ended runs took are sealed in place and the runs' readable copies removed
        (mail_attachments.py). The first time after a start covers every earlier run; with protection off, sealed
        attachments are opened again instead."""
        last = self.__dict__.get('attachments_swept')
        if last and time.monotonic() - last[0] < every:
            return
        started, store = now(), next_actions.attachment_store(self.config)
        if not last and not self.store.protected and (opened := mail_attachments.open_all(self.config, store)):
            LOG.info('email attachments opened: %s', opened)
        if (sealed := mail_attachments.sweep(self.store.connect, self.config, since=last[1] if last else None, store=store)):
            LOG.info('email attachments sealed: %s', sealed)
        self.attachments_swept = (time.monotonic(), started)

    def flag_browser_waits(self):
        """A sent card is redrawn once when its running preparation starts waiting on the browser, so it says so and,
        with a viewer link, gets its Open the browser button. A blocked one is redrawn anyway."""
        flagged = self.__dict__.setdefault('browser_flagged', set())
        with self.store.connect() as db:
            # A blocked sign-in is redrawn once too (once per start), so a card from before gets its Sign in button.
            for job in db.execute("SELECT job_id,suggestion_id,status,reason FROM preparations WHERE status IN ('starting','running','blocked')").fetchall():
                if job['job_id'] in flagged or (job['status'] == 'blocked' and not signin_handoff(job['reason'])) or not browser_wait(db, job['job_id'], job['status'], reason=job['reason']):
                    continue
                flagged.add(job['job_id'])
                db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (job['suggestion_id'],))

    def signin_waits(self):
        """Blocked preparations of open tasks that wait on the owner to sign in: [(suggestion_id, job_id, page)]."""
        found = []
        with self.store.connect() as db:
            for job in db.execute("SELECT p.suggestion_id,p.job_id,p.reason FROM preparations p JOIN suggestions s ON s.id=p.suggestion_id "
                                  f"WHERE p.status='blocked' AND s.status IN {todo_states.sql(todo_states.PREPARING)}").fetchall():
                waiting = signin_handoff(job['reason']) and browser_wait(db, job['job_id'], 'blocked', reason=job['reason'])
                if waiting:
                    found.append((job['suggestion_id'], job['job_id'], waiting.get('page')))
        return found

    def signin_reason(self, suggestion_id):
        with self.store.connect() as db:
            row = db.execute("SELECT reason FROM preparations WHERE suggestion_id=? AND status='blocked'", (suggestion_id,)).fetchone()
        return row[0] if row else None

    def signin_tabs(self):
        """The shared browser's open pages, [{id, url}] (DevTools on loopback only)."""
        base = browser_login.endpoints(self.config)[0]
        return [{'id': t.get('id'), 'url': t.get('url') or ''} for t in browser_login.browser_cdp._http(base, '/json/list', timeout=3) if t.get('type') == 'page']

    def signin_open(self, suggestion_id):
        """The sign-in dialog for a task: its sign-in page in front in the shared browser, reopened from the address
        its own run left off at when that tab is gone. Returns what the dialog shows: {state, site, kind, view}."""
        page = self.signin_page(suggestion_id)
        view = browser_link(self.config)
        if not page:
            return {'state': 'unknown', 'site': None, 'kind': None, 'view': view}
        reason = self.signin_reason(suggestion_id)
        opened = self.__dict__.setdefault('signin_opened', {})
        try:
            tabs = self.signin_tabs()
        except (browser_login.browser_cdp.CdpError, OSError, TypeError, AttributeError):
            raise OwnerError('I couldn’t reach the browser on this computer') from None
        mine = [t for t in tabs if t['id'] == opened.get(suggestion_id)] + [t for t in tabs if same_site(t['url'], page)]
        if mine:  # followed from here on, also through an identity provider on another host
            state, url, opened[suggestion_id] = 'open', mine[0]['url'], mine[0]['id']
        else:
            url = site_language(page, self.config)  # LinkedIn's in the owner's language
            try:
                opened[suggestion_id] = browser_login.browser_cdp.open_tab(browser_login.endpoints(self.config)[0], url)
            except (browser_login.browser_cdp.CdpError, OSError):
                raise OwnerError('I couldn’t open the sign-in page in the browser') from None
            state = 'opened'
        try:
            browser_viewer.focus(url, browser_login.endpoints(self.config)[0])
        except (ValueError, OSError):
            pass
        return {'state': state, 'site': signin_name(reason, page), 'kind': signin_kind(reason, [url]), 'view': view}

    def browser_show(self, suggestion_id):
        """View in browser: the page a task's own run worked on, in front in the Machine's browser (its own tab, still as
        the run left it), else reopened there from the address the run recorded. Never the owner's own browser and
        never another task's tab. Returns {shown, opened, site, view}: `view` is the browser's viewer, when there is one."""
        with self.store.connect() as db:
            page = task_page(db, suggestion_id)
        view = browser_link(self.config)
        if not page:
            return {'shown': False, 'unknown': True, 'view': view}
        base = browser_login.endpoints(self.config)[0]
        site = browser_login.site(urllib.parse.urlsplit(page['url']).hostname)
        try:
            tabs = self.signin_tabs()
        except (browser_login.browser_cdp.CdpError, OSError, TypeError, AttributeError):
            return {'shown': False, 'site': site, 'view': view, 'error': 'I couldn’t reach the browser on this computer'}
        same_port = page['target'] and urllib.parse.urlsplit(base).port == page['port']
        tab = (next((t for t in tabs if same_port and t['id'] == page['target']), None)
               or next((t for t in tabs if t['url'] == page['url']), None))
        opened = False
        if not tab:  # the tab is gone: the same address again, in the Machine's browser
            try:
                url = site_language(page['url'], self.config)
                tab = {'id': browser_login.browser_cdp.open_tab(base, url), 'url': url}
            except (browser_login.browser_cdp.CdpError, OSError):
                return {'shown': False, 'site': site, 'view': view, 'error': 'I couldn’t open that page in the browser'}
            opened = True
        try:
            shown = browser_viewer.focus(tab['url'], base, target=tab['id']) is not None
        except (ValueError, OSError):
            shown = False
        return {'shown': shown, 'opened': opened, 'site': site, 'view': view}

    def task_front(self, page):
        """Open the browser for a preparing card: the tab on the task's page (same site) in front in the Machine's
        browser, and when the run's tab is gone, that page opened again there, so the owner never lands on a closed or
        unrelated tab. Returns {shown, opened}."""
        base = browser_login.endpoints(self.config)[0]
        opened = None
        try:
            if not any(same_site(t['url'], page) for t in self.signin_tabs()):
                opened = browser_login.browser_cdp.open_tab(base, page)
        except (browser_login.browser_cdp.CdpError, OSError, TypeError, AttributeError, ValueError):
            pass  # can't read the tabs: bring what there is to the front, as before
        try:
            shown = browser_viewer.focus(page, base, target=opened)
        except (ValueError, OSError):
            shown = None
        return {'shown': shown is not None, 'opened': bool(opened)}

    def signin_page(self, suggestion_id):
        """The address a task's blocked sign-in waits on, from its own run steps (run_page), or None."""
        return next((page for task, job, page in self.signin_waits() if task == suggestion_id), None)

    def resume_signed_in(self, host=None, suggestion_id=None, source='signed_in'):
        """Carries on the tasks blocked on a sign-in that is now done: the one named, and those waiting on `host`'s site.
        The same as tapping Continue; nothing here signs in or touches the site. Returns the resumed task ids."""
        resumed = []
        for task, job, page in self.signin_waits():
            # Keyed on each task's own site: a sign-in elsewhere never carries a task on, named or not.
            if not (bool(page) and same_site(host, page) if host else task == suggestion_id):
                continue
            try:
                self.store.decide(task, 'retry', '', 'signed-in:' + job, source)
            except ValueError as error:
                LOG.info('sign-in resume skipped suggestion=%s error=%s', task, error)
                continue
            LOG.info('sign-in resume suggestion=%s source=%s', task, source)
            resumed.append(task)
        return resumed

    def watch_sign_ins(self, every=SIGNIN_WATCH, now=False):
        """Signing in in the browser itself carries on too. While a task waits on a sign-in, look every `every` seconds
        at the shared browser (read-only: which sign-in fields show, never what is in them, and the tabs' addresses).
        The task's site was seen at its sign-in (a form, a sign-in address, its identity provider) and now a tab of it
        is past that with no form: the owner got in, so carry on, once per blocked run. Also for sign-ins with
        nothing to type (itsme or eID, a passkey, a captcha, choosing an account). `now`: look at once (the owner just
        closed the browser). Returns the tasks it carried on."""
        state = self.__dict__.setdefault('signin_watch', {'next': 0.0, 'seen': set(), 'done': set()})
        if time.monotonic() < state['next'] and not now:
            return []
        state['next'] = time.monotonic() + every
        waits = [(task, job, page) for task, job, page in self.signin_waits() if page and job not in state['done']]
        if not waits:
            state['seen'].clear()
            return []
        try:
            shown = [p['host'] for p in browser_login.pages(self.config)]
            tabs = self.signin_tabs()
        except Exception:  # no browser right now: look again later
            return []
        resumed = []
        opened = self.__dict__.get('signin_opened', {})
        for task, job, page in waits:
            mine = [t['url'] for t in tabs if t['id'] == opened.get(task) or same_site(t['url'], page)]
            if any(same_site(host, page) for host in shown) or any(signin_address(url, page) for url in mine):
                state['seen'].add(job)
            elif job in state['seen'] and any(same_site(url, page) for url in mine):
                state['seen'].discard(job)
                state['done'].add(job)
                resumed += self.resume_signed_in(suggestion_id=task)
        return resumed

    def release_finished_browser_lease(self, lease_file=BROWSER_LEASE):
        """A Do it run holds the browser as `assistant-<first 8 of its job ID>`. Runs can end without
        releasing it (October 13: one blocked itself on its own lease), so free each such holder whose
        run is no longer starting or running. Other owners' leases are never touched. The lease is
        shared since 2026-10-13 (`holders`); the older single `owner` format is still read."""
        try:
            state=json.loads(Path(lease_file).read_text())
            owners=list(state.get('holders') or {})+([state['owner']] if state.get('owner') else [])
        except (OSError,ValueError,AttributeError,TypeError):return False
        released=False
        for owner in owners:
            match=re.fullmatch(r'assistant-([a-f0-9]{8})',str(owner))
            if not match:continue
            with self.store.connect() as db:
                known=db.execute("SELECT finished_at FROM preparation_runs WHERE substr(job_id,1,8)=?",(match[1],)).fetchall()
                if not known or any(not r['finished_at'] for r in known):
                    continue
            subprocess.run([sys.executable,str(browser_lease_script(self.config)),'release','--owner',owner],
                           capture_output=True,timeout=30)
            LOG.info('browser lease released owner=%s (run ended)',owner)
            released=True
        return released
