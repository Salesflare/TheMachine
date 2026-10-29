"""Help and Report a bug, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

Its actions are the owner's own, from their dashboard only. SUPPORT_ACTIONS in assistant.py stays the reviewed list of
them (the security boundary); ACTIONS here says which method handles each. support_action itself stays in assistant.py
for now: it uses the model helpers (has_model, background_model), which move out of assistant.py first."""
import logging
import os
import threading

import bug_queue

LOG = logging.getLogger('personal-assistant')


class SupportApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = dict.fromkeys(('bug_fixed', 'bug_later', 'bug_preview', 'bug_queued', 'bug_send', 'help_article',
                             'help_ask', 'support_access'), 'support_dashboard_action')

    def support_dashboard_action(self, name, args, owner_dashboard):
        if not owner_dashboard:
            raise ValueError('Help and bug reports come from the dashboard')
        return self.support_action(name, args)

    def bug_queue_worker(self):
        """Report a bug: the reports the control plane couldn't take yet go out when they are due (bug_queue.py),
        looked at every 30 seconds."""
        self.bug_queue_wake = getattr(self, 'bug_queue_wake', None) or threading.Event()
        while not self.stop.is_set():
            try:
                bug_queue.flush(self.config, self.bug_with_report)
            except Exception as error:  # noqa: BLE001 - never stops the service
                LOG.error('bug queue error=%s', type(error).__name__)
            self.bug_queue_wake.wait(30)
            self.bug_queue_wake.clear()

    REPORT_BUDGET = 20  # seconds the support report may take; a part not ready by then goes without (support.report)

    def bug_with_report(self, body):
        """A kept report sent (bug_queue.flush): one whose owner ticked Include a support report gets it now, scrubbed
        and built within REPORT_BUDGET. When the report can't be built, what the owner wrote still goes, with why."""
        import onboarding
        import support
        body = dict(body)
        if body.pop('diagnostics', False) and body.get('report') is None:
            path = getattr(self, 'config_path', None) or os.environ.get('ASSISTANT_CONFIG') or ''
            try:
                found = support.report(path, doctor=onboarding.doctor, budget=self.REPORT_BUDGET)
                body['report'] = support.scrub_value({'parts': found['parts'], 'settings': found['settings']})
            except Exception as error:  # noqa: BLE001 - the bug report goes whatever happens to the support report
                LOG.warning('support report not built error=%s', type(error).__name__)
                body['report'] = {'parts': {'report': [f'not built: {type(error).__name__}']}}
        return self.fleet.bug_report(body)

    def support_read(self, what):
        """Support access on a paired self-hosted Machine (fleet.Fleet.support_round): the scrubbed support report's lines
        (logs) or support.snapshot (settings), the same the owner's Report a bug shows, read-only."""
        import onboarding
        import support
        path = getattr(self, 'config_path', None) or os.environ.get('ASSISTANT_CONFIG') or ''
        if what == 'logs':
            return {'parts': support.report(path)['parts']}
        return support.snapshot(path, doctor=onboarding.doctor)
