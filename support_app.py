"""Help and Report a bug, the App's part: a domain mixin of App (only assistant.py composes it; docs/code-map.md).

Its actions are the owner's own, from their dashboard only. SUPPORT_ACTIONS in assistant.py stays the reviewed list of
them (the security boundary); ACTIONS here says which method handles each, and support_action
answers them."""
import logging
import os
import re
import sqlite3
import threading

import bug_queue
import chat_model
import fleet
import help_topics
import i18n
from models import background_model, has_model

LOG = logging.getLogger('personal-assistant')


class SupportApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = dict.fromkeys(('bug_fixed', 'bug_later', 'bug_offer_open', 'bug_preview', 'bug_queued', 'bug_send', 'help_article',
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

    def support_action(self, name, args):
        """Help's question (help_chat.ask, on this Machine's own model, a one-shot turn without tools) and Report a
        bug: the scrubbed support report to show (bug_preview), then that report sent to the control plane on a
        self-hosted Machine paired with the Network (bug_send). A hosted Machine's dashboard sends it to its control
        plane itself, with the owner's sign-in there."""
        import help_chat
        import onboarding
        import support
        if name == 'help_article':
            return help_chat.article(args.get('slug'))
        if name == 'help_ask':
            run = getattr(self, 'help_model', None)  # a stand-in in the sandbox and tests
            if not run and not has_model(self.config):
                raise ValueError(i18n.t('Help needs a model. Set one up in Settings, Model.'))
            swap = background_model(self.config)
            model, thinking = '/'.join(swap) if swap else None, None
            own = chat_model.clean({'model': args.get('model'), 'thinking': args.get('thinking')})
            if chat_model.chosen(self.config, own):  # a model picked for Help or for chats (chat_model.py)
                models = self.chat_models()
                picked = chat_model.resolve(self.config, models, chat_model.check(own, models, self.config) if own else {})
                model, thinking = picked['model'] or model, picked['thinking']
            try:
                found = help_chat.ask(args.get('question'), args.get('history') or [], run=run, config=self.config,
                                      model=model, thinking=thinking, role=self.owner_role())
            except help_chat.Unavailable as error:
                raise ValueError(str(error)) from None
            topic, answered = found.pop('topic', ''), found.pop('answered', False)
            try:  # the topic for The Machine team, when the owner shares it (help_topics.py); never the question
                if not getattr(self, 'fleet', None):
                    return found  # without the Network nothing goes, so nothing is kept
                with self.store.connect() as db:
                    help_topics.record(db, self.config, topic, answered)
            except (sqlite3.Error, ValueError) as error:
                LOG.info('help topic not kept error=%s', type(error).__name__)
            return found
        path = getattr(self, 'config_path', None) or os.environ.get('ASSISTANT_CONFIG') or ''
        if name == 'support_access':
            if not getattr(self, 'fleet', None):
                raise ValueError('This Machine isn’t linked to an account.')
            allow = args.get('allow')
            try:
                return self.fleet.support_access(None if allow is None else bool(allow))
            except (fleet.Off, OSError, ValueError) as error:
                LOG.info('support access not reached error=%s', type(error).__name__)
                if allow is None:
                    return {'until': self.fleet.support_until(), 'hours': self.fleet.SUPPORT_HOURS, 'accesses': [], 'error': True}
                raise ValueError('Can’t reach your account right now. Try again.') from None
        if name == 'bug_preview':
            return {**support.report(path, doctor=onboarding.doctor, budget=self.REPORT_BUDGET), 'paired': bool(getattr(self, 'fleet', None))}
        if name == 'bug_fixed':  # a bug the owner reported, fixed and running here now (fleet.Fleet.fixed); seen closes one
            if not getattr(self, 'fleet', None):
                return {'fixed': []}
            try:
                return {'fixed': self.fleet.fixed(args.get('seen') or None)}
            except (fleet.Off, fleet.Unavailable, OSError, ValueError) as error:
                LOG.info('fixed reports not read error=%s', type(error).__name__)
                return {'fixed': [], 'error': True}
        if name == 'bug_queued':  # the reports still waiting to go out (bug_queue.py)
            return {'queued': bug_queue.view(self.config)}
        if name == 'bug_offer_open':  # a report written up in chat (bug_offer), to fill Report a bug; sent marks it sent
            found = bug_queue.offered(self.config, str(args.get('id') or '') or None, args.get('sent') is True)
            return {'offer': {k: found[k] for k in ('id', 'words', 'summary', 'sent')} if found else None}
        text = str(args.get('description') or '').strip()[:self.BUG_TEXT]
        if not text:
            raise ValueError('Say what went wrong first.')
        shot = args.get('screenshot')
        if shot is not None and not (isinstance(shot, str) and re.fullmatch(r'data:image/(png|jpeg|webp);base64,[A-Za-z0-9+/=]+', shot)
                                     and len(shot) <= self.BUG_SHOT_BYTES * 4 // 3 + 64):
            raise ValueError('That screenshot can’t be sent. Try a smaller PNG or JPEG.')
        report = args.get('report')
        if report is not None and not isinstance(report, dict):
            raise ValueError('That report can’t be sent.')
        if not getattr(self, 'fleet', None):
            raise ValueError('This Machine isn’t linked to an account. Email support@themachine.computer instead.')
        # What the owner saw, scrubbed once more here: whatever the page sent, nothing else leaves
        body = {'description': text, 'screenshot': shot,
                'report': support.scrub_value(report) if report is not None else None}
        # Sent now, or kept here and sent by itself later when the control plane can't take it now (bug_queue.py):
        # bug_later is a hosted dashboard's report its control plane refused for now, kept the same way
        # Include a support report ticked, on a self-hosted Machine: kept here at once (it is never lost) and sent by the
        # worker right away, with the report built there; the dashboard doesn't wait for the checks and logs.
        if name == 'bug_send' and args.get('diagnostics') and report is None:
            item = bug_queue.add(self.config, {**body, 'diagnostics': True}, now=True)
            if getattr(self, 'bug_queue_wake', None):
                self.bug_queue_wake.set()
            return {'sent': True, 'id': item['id']}
        retry_after = 0
        if name == 'bug_later':
            try:
                retry_after = max(0, min(int(args.get('retry_after') or 0), 86400))
            except (TypeError, ValueError):
                retry_after = 0
        else:
            try:
                return {'sent': True, **(self.fleet.bug_report(body) or {})}
            except Exception as error:  # noqa: BLE001 - said to the owner below
                LOG.info('bug report not sent now error=%s', type(error).__name__)
                if not bug_queue.retryable(error):
                    said = str(error)  # the control plane's reason when it is one for the owner (a sentence), else ours
                    raise ValueError(said if said.endswith('.') else 'The report didn’t go out. Email support@themachine.computer.') from None
                retry_after = getattr(error, 'retry_after', 0)
        item = bug_queue.add(self.config, body, retry_after)
        if getattr(self, 'bug_queue_wake', None):
            self.bug_queue_wake.set()
        return {'sent': False, 'queued': True, 'at': item['next_at']}
