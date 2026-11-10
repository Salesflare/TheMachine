"""Birthdays from Facebook, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

When the Birthdays template runs on a Machine with a browser (the shared one the LinkedIn and X readers use), it
offers one to-do, once: Import birthdays from Facebook. Nothing happens until the owner taps Import there. Then, in a
thread of its own: the page in a tab of its own, scrolled and read, the tab closed (birthdays_facebook.py), and the to-do
shows what was found and who it matched. Only the owner's Save keeps them. Another import is the owner's tap again (Import
again on the to-do, also after Reopen).

Hosted Machines get it too: their browser is the same shared one, seen through the viewer, where the owner signs in to
Facebook themselves. A browser that isn't signed in is said on the to-do, with Sign in to Facebook (the dashboard's
sign-in dialog, connect_site_signin), and nothing is read until the owner is in."""
import datetime as dt
import logging
import secrets
import subprocess
import sys
import threading
import urllib.request

import birthdays_facebook
import browser_login
import enrichment
import i18n
import todo_areas
from machine.browser import browser_lease_script

LOG = logging.getLogger('personal-assistant')
OFFERED = 'birthdays_facebook:offered'  # enrich_prefs: the to-do was offered once (also when the owner said Not needed)
KIND = 'routine.facebook_birthdays'


class BirthdaysFacebookApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'birthdays_facebook': 'birthdays_facebook_action'}
    FACEBOOK_BIRTHDAYS = birthdays_facebook.PAGE  # tests point it at a made-up page

    def birthdays_facebook_base(self):
        """The shared browser's DevTools address when it answers, else None."""
        base = (browser_login.endpoints(self.config) or [None])[0]
        if not base:
            return None
        try:
            urllib.request.urlopen(base + '/json/version', timeout=5).close()
        except (OSError, ValueError):
            return None
        return base

    def birthdays_facebook_offer(self, run):
        """The to-do, once per Machine, when it has a browser. Returns its id, or None."""
        with self.store.connect() as db:
            if enrichment.pref(db, OFFERED):
                return None
        if not self.birthdays_facebook_base():
            return None
        accounts = self.config.get('accounts', [])
        account = next((a for a in accounts if todo_areas.area_of_account(a) == todo_areas.PERSONAL), None) or \
            next((a for a in accounts if todo_areas.area_of_account(a)), None)
        if not account:
            return None
        title = i18n.t('Import birthdays from Facebook')
        text = i18n.t('Reads the birthdays on Facebook’s birthdays page once, in The Machine’s browser. Nothing is saved before you say so.')
        key = 'birthdays-facebook'
        event_id = self.store.reviewed_event(account['id'], key, KIND, title, text,
                                             {'sender_display': i18n.t('Birthdays'), 'routine': run.get('routine_id'), 'facebook_birthdays': True})
        try:
            sid = self.store.suggest(key, title, text, [event_id], when='now', work=False, personal=True, owner_step=True)['id']
        except ValueError as error:
            LOG.info('facebook birthdays to-do not saved error=%s', type(error).__name__)
            return None
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if not birthdays_facebook.get(db, sid):
                birthdays_facebook.put(db, sid, 'new', {}, self.routines_stamp())
            enrichment.set_pref(db, OFFERED, sid)
        return sid

    def birthdays_facebook_spawn(self, target, *args):
        """In a thread of its own (tests run it inline: birthdays_facebook_inline)."""
        if getattr(self, 'birthdays_facebook_inline', False):
            return target(*args)
        threading.Thread(target=target, args=args, daemon=True, name='birthdays-facebook').start()

    def birthdays_facebook_action(self, name, args, owner_dashboard):
        """The owner's tap on the to-do: step read (Import, Try again, Import again) or save (Save on the preview)."""
        if not owner_dashboard:
            raise ValueError('Only the owner imports birthdays, on the dashboard')
        sid, step = str(args.get('suggestion_id') or ''), args.get('step')
        stamp = self.routines_stamp()
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            got = birthdays_facebook.get(db, sid)
            row = db.execute('SELECT status FROM suggestions WHERE id=?', (sid,)).fetchone()
            if not got or not row or row['status'] == 'rejected':
                raise ValueError('That to-do is gone')
            state = birthdays_facebook.view(db, sid)['state']
            if step == 'read':
                if state == 'reading':
                    return {'state': 'reading'}
                birthdays_facebook.put(db, sid, 'reading', {}, stamp)
            elif step == 'save':
                if state != 'preview':
                    raise ValueError('Import again first')
                people = birthdays_facebook.save(db, got[1], stamp)
                saved = len(people)
                birthdays_facebook.put(db, sid, 'saved', {'saved': saved, 'people': people}, stamp)  # the rest read goes with the preview
            else:
                raise ValueError('step is read or save')
        if step == 'read':
            self.birthdays_facebook_spawn(self.birthdays_facebook_read, sid)
            return {'state': 'reading'}
        if row['status'] not in ('completed', 'rejected'):
            self.store.decide(sid, 'complete', '', 'facebook-birthdays-saved:' + sid + ':' + stamp, 'dashboard')
        return {'state': 'saved', 'saved': saved, 'people': people[:birthdays_facebook.SHOWN]}

    def birthdays_facebook_read(self, sid):
        """The read itself, under the shared browser lease, then the preview (or why there is none) on the to-do."""
        state, data = 'failed', {}
        owner = 'facebook-birthdays-' + secrets.token_hex(6)
        lease = [sys.executable, str(browser_lease_script(self.config))]
        claimed = False
        try:
            base = self.birthdays_facebook_base()
            if base:
                claim = subprocess.run([*lease, 'claim', '--owner', owner, '--minutes', '8', '--wait', '1'], capture_output=True, text=True, timeout=90)
                claimed = claim.returncode == 0
            if claimed:
                result = birthdays_facebook.read(base, self.FACEBOOK_BIRTHDAYS)
                if result.get('error') == 'signed-out':
                    state = 'signed_out'
                else:
                    with self.store.connect() as db:
                        data = birthdays_facebook.preview(db, result.get('items'), dt.datetime.now().date(),
                                                         result.get('capped'), result.get('missing'))
                    state = 'preview' if data['found'] else 'failed'
                    data = data if data['found'] else {'empty': True}
        except Exception as error:  # noqa: BLE001 - whatever went wrong, the to-do says it didn't work
            LOG.info('facebook birthdays read failed error=%s', type(error).__name__)
        finally:
            if claimed:
                try:
                    subprocess.run([*lease, 'release', '--owner', owner], capture_output=True, text=True, timeout=30)
                except (OSError, subprocess.SubprocessError):
                    pass  # the lease runs out by itself
        with self.store.connect() as db:
            birthdays_facebook.put(db, sid, state, data, self.routines_stamp())
        return state
