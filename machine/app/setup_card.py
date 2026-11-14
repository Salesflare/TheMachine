"""The setup to-do at the top of To-dos, "Get more out of The Machine" (dashboard/setup-card.js): what the Machine knows
about each step (setup_card), a row closed with its × (setup_dismiss) and brought back (setup_restore), and the phone
app's store links with their QR code (phone_app_nudge). The setup hints stay in assistant.py for now: they read the
reminder channels. A mixin of assistant.App (APP_MIXINS) for the two actions."""
import re
import sqlite3

from machine.delivery.push import (
    phone_qr,
)
from machine.owner_error import OwnerError


class SetupCardApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'setup_dismiss': 'setup_card_action', 'setup_restore': 'setup_card_action'}

    def setup_card_action(self, name, args, owner_dashboard):
        """A row's × or the card's (setup_dismiss), Undo, Show hidden or Settings' Show again (setup_restore): the
        owner's own dashboard only."""
        if not owner_dashboard:
            raise OwnerError('Only the owner closes a setup step, on the dashboard' if name == 'setup_dismiss'
                             else 'Only the owner brings back a setup step, on the dashboard')
        return (setup_dismiss if name == 'setup_dismiss' else setup_restore)(self.store, self.config, args.get('step'))


# The mobile app (iOS and Android), live in both stores: their links, and a page with both (its help article, for the
# docs). The setup to-do's phone row opens this phone's store; on a computer it shows a QR code and both store links.
# The code is `get`: one address that sends an iPhone to the App Store, an Android phone to Google Play and a computer
# to the help article (one code per store if it is ever unset). Never inside the app.
PHONE_APP_STORE = {'published': True, 'ios': 'https://apps.apple.com/app/id6829875215',
                   'android': 'https://play.google.com/store/apps/details?id=computer.themachine.app',
                   'page': 'https://themachine.computer/help/mobile-app', 'get': 'https://themachine.computer/app'}


def phone_app_nudge(store):
    """The mobile app for the setup to-do, or None while it isn't published: its https store links with a QR code for
    each (qr, or qr_ios and qr_android; rows of 0 and 1), and how many phones have it (none on a Machine without the
    app's push yet)."""
    if not PHONE_APP_STORE.get('published'):
        return None
    links = {k: PHONE_APP_STORE.get(k) for k in ('ios', 'android', 'get') if str(PHONE_APP_STORE.get(k) or '').startswith('https://')}
    codes = {'qr': links.pop('get')} if 'get' in links else {'qr_' + k: links[k] for k in ('ios', 'android') if k in links}
    out = dict(links)
    for key, link in codes.items():
        try:
            out[key] = list(phone_qr(link))
        except ValueError:  # too long for a code: the store links alone
            pass
    try:
        with store.connect() as db:
            phones = db.execute('SELECT count(*) FROM notify_app_devices').fetchone()[0]
    except sqlite3.Error:
        phones = 0
    return {**out, 'phones': phones}


# The setup to-do at the top of To-dos, "Get more out of The Machine" (dashboard/setup-card.js): a row per step, in this
# order, each ticked once done and closed for good with its ×, the whole to-do with its own ×. What the Machine knows
# about each step is here; what only a device knows (its notifications, the app installed there) the dashboard works
# out itself. Closed rows are kept on the Machine (milestones 'setup:<step>'), so every device agrees.
SETUP_STEPS = ('calendar', 'phone', 'push', 'whatsapp', 'install', 'account', 'connect')


SETUP_STEP_RE = re.compile(r'(?:' + '|'.join(SETUP_STEPS) + r'|card|hint-[a-z0-9-]{1,40})')


SETUP_BASIC = {'gmail', 'outlook', 'calendar', 'outlook_calendar', 'whatsapp'}  # the connect row: anything beyond these


def setup_card(store, config):
    """{closed, dismissed, phones, whatsapp, calendar, mail_accounts, add, more, since} for the setup to-do: closed with
    its × (for good), the rows closed, phones with the app, a WhatsApp connected, a calendar connected (Google's or
    Outlook's), how many mail accounts (another one: add, the provider the owner has), a connection beyond mail, calendar
    and WhatsApp (more), and since when the owner has had to-dos (the first one shown, else when this Machine started
    counting): after that first day the dashboard folds the to-do into one line. The owner's own accounts only."""
    services = [str(a.get('service') or '') for a in config.get('accounts') or [] if isinstance(a, dict) and not a.get('shared')]
    with store.connect() as db:
        closed = {r['name'][6:] for r in db.execute("SELECT name FROM milestones WHERE name LIKE 'setup:%'")}
        at = dict(db.execute("SELECT name,at FROM milestones WHERE name IN ('first_card_shown','tracking_since')").fetchall())
        try:
            phones = db.execute('SELECT count(*) FROM notify_app_devices').fetchone()[0]
        except sqlite3.Error:
            phones = 0
    mail = [s for s in services if s in ('gmail', 'outlook', 'imap')]
    return {'closed': 'card' in closed, 'dismissed': sorted(closed - {'card'}), 'phones': phones, 'whatsapp': 'whatsapp' in services,
            'calendar': any(s in ('calendar', 'outlook_calendar', 'icloud_calendar', 'caldav', 'proton_calendar', 'ics', 'exchange') for s in services),
            'mail_accounts': len(mail), 'add': 'microsoft' if 'outlook' in mail and 'gmail' not in mail else 'google',
            'more': any(s and s not in SETUP_BASIC for s in services),
            'since': at.get('first_card_shown') or at.get('tracking_since') or None}


def setup_dismiss(store, config, step):
    """A row of the setup to-do closed with its × (a step, or a setup hint: hint-<id>), or the whole to-do (card): it
    never comes back, on any device."""
    step = str(step or '')
    if not SETUP_STEP_RE.fullmatch(step):
        raise ValueError('Unknown setup step')
    store.setup_closed(step)
    return {'setup_card': setup_card(store, config)}


def setup_restore(store, config, step):
    """A closed row of the setup to-do back (Undo after its ×), the whole to-do back (card), or everything closed back
    (all: Show hidden, or Settings, General, Setup to-do). Returns the setup to-do as it is now."""
    step = str(step or '')
    if step != 'all' and not SETUP_STEP_RE.fullmatch(step):
        raise ValueError('Unknown setup step')
    store.setup_closed(step, closed=False)
    return {'setup_card': setup_card(store, config)}
