"""Settings, Notifications (App.action): what reaches the owner and when, a page saying it is in use, a test
notification, and the phone's and browser's push subscriptions. Moved out of assistant.App's action as is. A mixin of
assistant.App (APP_MIXINS)."""
import re

import i18n
from machine.delivery.push import app_wake, push_send
import notify
from timeutil import now


class NotificationsApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'notify_set': 'notify_action', 'notify_active': 'notify_action', 'notify_preview': 'notify_action',
               'push_test': 'push_test_action', 'app_push_register': 'app_push_action_handler',
               'app_push_unregister': 'app_push_action_handler', 'push_subscribe': 'push_subscribe_action',
               'push_unsubscribe': 'push_subscribe_action'}

    def notify_action(self, name, args, owner_dashboard=False):
        # Settings, Notifications (notify.py)
        if not owner_dashboard:
            raise ValueError('Notifications are set in the dashboard')
        if name == 'notify_active':  # a page says whether it is in use (visible, in focus, touched lately) or not
            client = str(args.get('client') or 'page')
            if not re.fullmatch(r'[a-z0-9]{1,16}', client):
                raise ValueError('Invalid page')
            on = args.get('active', True) is not False
            try:
                idle = max(0, min(int(args.get('idle') or 0), 86400))
            except (TypeError, ValueError):
                idle = 0
            notify.mark_active(client=client, on=on, idle=idle)
            return {'active': notify.active()}
        if name == 'notify_preview':  # shown on the page only: nothing is sent
            digest = self.digest()
            return {'empty': not digest, 'text': digest['text'] if digest else '', 'push': digest['push'] if digest else None}
        with self.store.connect() as db:
            notify.set_pref(db, str(args.get('kind') or ''), str(args.get('channel') or ''), bool(args.get('on')))
        return self.notify_view()

    def push_test_action(self, name, args, owner_dashboard=False):
        # Settings or the nudge: one test notification to this device's own subscription
        if not owner_dashboard:
            raise ValueError('Phone notifications are turned on in the dashboard app')
        if 'app_device' in args:  # the mobile app: a test wakeup to that phone only
            device = str(args.get('app_device') or '')
            with self.store.connect() as db:
                known = notify.APP_ID.fullmatch(device) and any(d['id'] == device for d in notify.app_devices(db))
            if not known:
                raise ValueError('Notifications are off on this device. Turn them on first.')
            if not app_wake(self.store, self.config, 'test', 'push-test', device):
                raise ValueError('The test didn’t go through. Turn notifications off and on again.')
            return {'sent': True}
        with self.store.connect() as db:
            row = db.execute('SELECT endpoint,p256dh,auth FROM push_subscriptions WHERE endpoint=?', (str(args.get('endpoint') or ''),)).fetchone()
        if not row:
            raise ValueError('Notifications are off on this device. Turn them on first.')
        results = push_send(self.store, self.config, [dict(row)], {'title': i18n.t('Notifications are on'), 'body': i18n.t('This is how a new to-do shows up.'), 'url': '.', 'tag': 'push-test'}, 'test')
        if not any(200 <= r.get('status', 0) < 300 for r in results):
            raise ValueError('The test didn’t go through. Turn notifications off and on again.')
        return {'sent': True}

    def app_push_action_handler(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Phone notifications are turned on in the dashboard app')
        return self.app_push_action(name, args)

    def push_subscribe_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Phone notifications are turned on in the dashboard app')
        endpoint = str(args.get('endpoint') or '')
        if not re.fullmatch(r'https://[^\s]{1,2000}', endpoint):
            raise ValueError('Invalid push subscription')
        with self.store.connect() as db:
            if name == 'push_unsubscribe':
                db.execute('DELETE FROM push_subscriptions WHERE endpoint=?', (endpoint,))
                return {'subscribed': False}
            keys = args.get('keys') or {}
            if not all(re.fullmatch(r'[A-Za-z0-9_-]{16,200}=*', str(keys.get(k) or '')) for k in ('p256dh', 'auth')):
                raise ValueError('Invalid push subscription')
            db.execute('''INSERT INTO push_subscriptions(endpoint,p256dh,auth,created_at) VALUES(?,?,?,?)
                    ON CONFLICT(endpoint) DO UPDATE SET p256dh=excluded.p256dh,auth=excluded.auth''',
                       (endpoint, keys['p256dh'].rstrip('='), keys['auth'].rstrip('='), now()))
        return {'subscribed': True}
