"""Check now in the service (check_now.py has the check itself): the action, the collectors' early wake, and the status
the To-dos head shows (docs/help/cards.md#check-now). A mixin of assistant.App (APP_MIXINS)."""
import logging
import threading
import time

import check_now
LOG = logging.getLogger('personal-assistant')


class CheckNowApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'check_now': 'check_now_action'}

    def check_now_action(self, name, args, owner_dashboard):
        """Check now: the To-dos page head, the phone app, or chat (assistant check); {'status': True} only looks."""
        return {'check': self.check_view()} if args.get('status') is True else self.check_start()

    def collector_rest(self, account_id, seconds):
        """A collector's wait until its next read; ends early on stop or when Check now wakes it (wake_collectors)."""
        wakes = self.__dict__.get('collector_wakes')
        if wakes is None:  # an App made without __init__ (a test's): no Check now
            self.stop.wait(seconds)
            return
        wake = wakes.setdefault(account_id, threading.Event())
        wake.clear()
        end = time.monotonic() + seconds
        until = self.__dict__.setdefault('collector_rest_until', {})  # history's Slack lane reads only with room before it
        until[account_id] = end
        self.collector_resting.add(account_id)
        try:
            while not self.stop.is_set() and (left := end - time.monotonic()) > 0:
                if wake.wait(min(left, 60)):
                    return
        finally:
            self.collector_resting.discard(account_id)
            until.pop(account_id, None)

    def wake_collectors(self, wanted):
        """Check now (check_now.run): every resting collector whose account `wanted` takes reads now. Returns their ids;
        one waiting out an error, or reading already, isn't woken."""
        woken = []
        for account in self.config.get('accounts') or []:
            if account.get('id') in self.collector_resting and wanted(account):
                self.collector_wakes[account['id']].set()
                woken.append(account['id'])
        LOG.info('check now: woke %d sources', len(woken))
        return woken

    def check_start(self):
        """Check now, from the dashboard, the phone app or chat (`assistant check`): a new check, or the one running or
        just ended (check_now.Check.start), so repeated presses never stack."""
        view = self.check_view() or {}
        if not self.check.phase() and (view.get('reviewing') or view.get('reading')):
            return {'started': False, 'check': view}  # a review or a first import runs already: it brings what a check would
        started = self.check.start(time.time())
        if started:
            threading.Thread(target=check_now.run, args=(self.check, self), name='check-now', daemon=True).start()
        return {'started': started, 'check': self.check_view()}

    def mail_check_view(self):
        """The line on To-dos after a check that saw new messages, from any source (check_now.mail_check): what it read
        and why nothing needed the owner."""
        try:
            own = [a.get('email') for a in self.config.get('accounts') or [] if a.get('email')]
            with self.store.connect() as db:
                return check_now.mail_check(db, own=own)
        except Exception as error:  # noqa: BLE001 - the dashboard shows without it
            LOG.error('mail check view error=%s', type(error).__name__)
            return None

    def check_view(self):
        try:
            with self.store.connect() as db:
                queue = self.review_queue(db)
                return self.check.view(check_now.reviews(db, queue, (self.config.get('review_worker') or {}).get('min_signals', 40)))
        except Exception as error:  # noqa: BLE001 - the dashboard shows without it
            LOG.error('check view error=%s', type(error).__name__)
            return None
