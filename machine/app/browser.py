"""The dashboard's browser actions (App.action): bringing the browser or a task's page to the front, and signing in to
sites through the encrypted login store (browser_login.py), where what the owner types never reaches a log, the model
or an error message. Moved out of assistant.App's action as is. A mixin of assistant.App (APP_MIXINS)."""
from pathlib import Path
import urllib.parse

import browser_login
import browser_viewer
from machine.browser import same_site
import security_levels


class BrowserApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'browser_focus': 'browser_focus_action', 'browser_show': 'browser_show_action',
               'browser_login_open': 'browser_login_action', 'browser_login_pages': 'browser_login_action',
               'browser_login_fill': 'browser_login_action', 'browser_login_choose': 'browser_login_action',
               'browser_login_check': 'browser_login_action', 'browser_logins': 'browser_login_action',
               'browser_login_forget': 'browser_login_action'}

    def browser_focus_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner brings the browser to the front, from the dashboard')
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
            raise ValueError('Only the owner opens a task’s page in the browser, from the dashboard')
        if not isinstance(args.get('suggestion_id'), str):
            raise ValueError('Which task?')
        return self.browser_show(args['suggestion_id'])

    def browser_login_action(self, name, args, owner_dashboard=False):
        # A separate path: what the owner types goes into the page and, when asked, the encrypted store, never
        # into a log, the model or an error message (see browser_login.py).
        if not owner_dashboard:
            raise ValueError('Only the owner signs in to sites, from the dashboard')
        logins = browser_login.LoginStore(Path(self.config['database']).expanduser().parent)
        if name == 'browser_login_open':
            if not isinstance(args.get('suggestion_id'), str):
                raise ValueError('Which task?')
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
            found =browser_login.pages(self.config, logins, args.get('account') if isinstance(args.get('account'), str) else None)
            if isinstance(args.get('suggestion_id'), str):
                # For a task, only the sign-in on the site its own run left off at; unknown: none, never a guess.
                page = self.signin_page(args['suggestion_id'])
                found = [p for p in found if page and same_site(p['host'], page)]
                return {'pages': found, 'task_site': browser_login.site(urllib.parse.urlsplit(page).hostname) if page else None}
            return {'pages': found}
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
                raise ValueError('Nothing is saved for ' + browser_login.site(host))
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
