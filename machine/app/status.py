"""The dashboard's status (App.action 'status'): the store's snapshot with where this install is managed, its account,
workers, health and what the page needs to draw itself; the agent's compact view of it, sign-in help for a signed-out
source, and what only the owner can fix (needs_you). Moved out of assistant.py as is. A mixin of assistant.App
(APP_MIXINS)."""
import json
from pathlib import Path
import sqlite3
import urllib.parse

import abilities
import agent_jobs
import fleet
from machine.app.setup_card import phone_app_nudge, setup_card
from machine.browser import browser_link
from machine.cards import snooze_choices
from machine.config import LOG, WORKSPACE
from machine.delivery.push import reminder_channels, reviews_start_by_themselves
from machine.sources.connectors import (connector_says, docs_offered, docs_provider, docs_unset, docs_write_offered,
                                        reconnect_help, SIGNIN_ONLY)
from machine.text import clamp
import message_seal
from models import main_model, model_ready
from sources import gog_signin_command


def agent_work_status(job):
    """A card's latest Claude Code or Codex job in the compact status: what it did (or is doing) and when."""
    if not isinstance(job, dict):
        return {}
    work = {'tool': job.get('name') or job.get('tool'), 'status': job.get('status'),
            'at': job.get('finished_at') or job.get('started_at') or job.get('created_at')}
    if str(job.get('summary') or '').strip():
        work['result'] = agent_jobs.gist(job['summary'], 500)
    if job.get('status') in ('running', 'waiting') and str(job.get('progress') or '').strip():
        work['progress'] = agent_jobs.gist(job['progress'], 200)
    if job.get('error'):
        work['error'] = clamp(job['error'], 200)
    return {'agent_work': work}


CLOSED = ('completed', 'rejected')


def compact_card(s):
    """One to-do in the agent's status. An open one with its first 400 characters; a done or dismissed one only as
    much as tells it is the same matter (title, dedupe_key, when it closed): its body was most of a review's status
    (about 20k tokens a read, 2026-11-08) and pushed the open to-dos past OpenClaw's tool-result cut."""
    if s.get('status') in CLOSED:
        return {**{k: s[k] for k in ('id', 'status', 'title', 'dedupe_key', 'closed_at') if s.get(k)}, **agent_work_status(s.get('agent_job'))}
    return {**{k: s[k] for k in ('id', 'status', 'title', 'dedupe_key', 'created_at', 'deliver_after', 'snoozed_until', 'latest_feedback', 'preparation_status', 'handled_hint') if s.get(k)},
            'body': clamp(s.get('body') or '', 400), **agent_work_status(s.get('agent_job'))}


def compact_status(result):
    """The agent's view of status, well under OpenClaw's tool-result cut: the open to-dos first, then the done ones in
    short. The CLI and dashboard read the full version."""
    keep = ('id', 'service', 'boundary', 'display_name', 'error', 'last_success', 'retry_at', 'failures_24h',
            'signals_24h', 'pending', 'total', 'deferred_threads', 'last_failure')
    cards = [s for s in result['suggestions'] if s.get('status') not in CLOSED] + [s for s in result['suggestions'] if s.get('status') in CLOSED]
    return {
        'review_health': result['review_health'],
        'suggestion_counts': result['suggestion_counts'],
        'connectors': [{k: clamp(c[k], 200) for k in keep if c.get(k) not in (None, '', 0, [], {})} for c in result['connectors']],
        'suggestions': [compact_card(s) for s in cards],
        'decisions': [{k: clamp(d[k], 300) for k in ('id', 'suggestion_id', 'choice', 'source', 'feedback', 'created_at') if d.get(k)} for d in result['decisions'][:30]],
        'recent_reviews': [{'started_at': a['started_at'], 'status': a['status'], 'checked': a.get('checked_count'),
                            'claimed': len(json.loads(a['items'] or '[]')), 'summary': clamp(a.get('summary') or a.get('last_error') or '', 300)}
                           for a in result['analyses'][:8]],
        'note': 'Compact view. Read signals with events; open suggestions show their first 400 characters, done ones their title. '
                'status with suggestion_id gives one suggestion in full.'}


def card_status(result, suggestion_id):
    """status with suggestion_id: that one to-do (its body in full) and the owner's decisions on it, for a to-do's own
    run (a preparation, Do it, its chat), which read the whole status (about 20k tokens) to find one card."""
    card = next((s for s in result['suggestions'] if s.get('id') == suggestion_id), None)
    if card is None:
        return {'suggestion': None, 'note': 'No such suggestion.'}
    keep = ('id', 'status', 'title', 'dedupe_key', 'created_at', 'closed_at', 'deliver_after', 'snoozed_until', 'latest_feedback',
            'preparation_status', 'handled_hint')
    return {'suggestion': {**{k: card[k] for k in keep if card.get(k)}, 'body': card.get('body') or '', **agent_work_status(card.get('agent_job'))},
            'decisions': [{k: clamp(d[k], 300) for k in ('id', 'suggestion_id', 'choice', 'source', 'feedback', 'created_at') if d.get(k)}
                          for d in result['decisions'] if d.get('suggestion_id') == suggestion_id][:30]}


def sign_in_help(service, error, manage):
    """For a source read through the shared browser that is signed out: where to sign in again (the hosted page that
    opens this server's browser on that site) or, without one, what to do in plain words."""
    if not (error or '').endswith('_signed_out'):
        return {}
    import onboarding
    try:
        setup = onboarding.setup_of(service)
    except Exception:
        return {}
    site = setup.get('browser')
    hint = next((text for prefix, text in (setup.get('hints') or {}).items() if error.startswith(prefix)), '')
    return {'signed_out': True, 'sign_in_hint': hint,
            'sign_in_url': urllib.parse.urljoin(manage, '/open?' + urllib.parse.urlencode({'to': 'browser', 'site': site}))
            if manage and site else None}


def needs_you(config):
    """What only the owner can fix, for the top of the dashboard: sources that are not fully set up, and notes that a
    hosting layer leaves in `needs_you_file` (a JSON list of {id, text, url}). Connections whose sign-in fails are added
    by the dashboard itself, from their sync errors."""
    import onboarding
    manage = str(config.get('manage_url') or '')
    manage = manage if manage.startswith('https://') else ''
    items = []
    for account in config.get('accounts', []):
        try:
            why = onboarding.missing(config, account)
            name = account.get('display_name') or account.get('email') or onboarding.label(account.get('service', 'gmail'))
        except Exception:
            continue
        if why:
            items.append({'id': 'setup-' + account['id'], 'text': f'{name} is not fully set up yet ({why}).',
                          'url': '#connections=add' if manage else None, 'action': 'Finish it' if manage else 'Run: assistant connect'})
    # The main model can't run (no sign-in or key for its provider): nothing gets reviewed, the first look neither
    model = main_model()
    if model and model_ready(config, wait=False) is False:  # the poll never waits on `openclaw models status`
        items.append({'id': 'model-signed-out', 'text': f'Your main model, {model}, can\u2019t run: nothing is signed in for it. '
                      'Nothing gets checked until it can.', 'url': manage + '#model' if manage else None,
                      'action': 'Fix it' if manage else 'Run: openclaw models auth login'})
    # The message key (message_seal.py): without it, the messages can't be read after a restart
    try:
        for key, text, fix in message_seal.problems(config['database']) if config.get('database') else []:
            items.append({'id': key, 'text': text, 'url': None, 'action': 'Run: ' + (fix if fix.startswith('chmod') else 'assistant doctor')})
    except OSError:
        pass
    # USER.md past what reviews and Do it runs read: one line, so the owner shortens it instead of losing its end unseen
    import onboarding
    size = onboarding.user_md_too_long(config.get('openclaw_workspace') or WORKSPACE)
    if size:
        items.append({'id': 'user-md-long', 'text': f'Your USER.md is {size:,} characters. Checks and Do it read the first '
                      f'{onboarding.USER_MD_CONTEXT_LIMIT:,}, so the end is left out.', 'url': None, 'action': None})
    # `needs_you_file`: optional JSON list of notes from a hosting layer (a hosted machine), shown as they are.
    path = config.get('needs_you_file')
    if path:
        try:
            notes = json.loads(Path(path).expanduser().read_text())
        except (OSError, ValueError):
            notes = []
        for note in notes if isinstance(notes, list) else []:
            if isinstance(note, dict) and isinstance(note.get('text'), str) and note['text'].strip():
                url = str(note.get('url') or '')
                items.append({'id': str(note.get('id') or len(items))[:80], 'text': note['text'][:500],
                              'url': url if url.startswith('https://') else None, 'action': str(note.get('action') or 'Open')[:40]})
    return items


class StatusApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'status': 'status_action'}

    def heartbeat_health(self, health):
        """Read only the existing heartbeat's runtime facts, never conversation
        content or scheduler configuration. Missing evidence stays unknown."""
        try:
            with sqlite3.connect('file:' + str(Path.home() / '.openclaw/state/openclaw.sqlite') + '?mode=ro', uri=True, timeout=1) as db:
                # `heartbeat_job_id`: the OpenClaw cron job id of the main heartbeat (optional).
                row = db.execute('SELECT state_json FROM cron_jobs WHERE job_id=?', (self.config.get('heartbeat_job_id', ''),)).fetchone()
                if row:
                    scheduler = json.loads(row[0])
                    reason = scheduler.get('lastError', '')
                    health['heartbeat'] = {k: scheduler.get(k) for k in ['lastRunAtMs', 'nextRunAtMs', 'lastRunStatus', 'consecutiveSkipped']}
                    health['heartbeat']['reason'] = 'busy' if reason in ['heartbeat skipped: cron-in-progress','heartbeat skipped: requests-in-flight','heartbeat skipped: active-run','heartbeat skipped: plugin-operation-in-progress','heartbeat skipped: runtime-draining'] else 'failed' if scheduler.get('lastRunStatus')=='error' else None
        except (sqlite3.Error, OSError, ValueError):
            pass

    def status_action(self, name, args, owner_dashboard=False):
        if not args.get('full'):  # an agent: only what compact_status reads, so it stays fast on a busy Machine
            return self.agent_status(str(args.get('suggestion_id') or '').strip() or None)
        # done: how many done to-dos (the dashboard: its Done list's first page, it loads the rest itself); else the last 100
        done = args.get('done')
        result = self.store.snapshot(self.config['accounts'], **({'done': max(0, min(int(done), 100))} if isinstance(done, int) else {}))
        # `manage_url`: where this install is set up when that is a web page (a hosted machine); the dashboard links to it.
        manage = str(self.config.get('manage_url') or '')
        result['manage_url'] = manage if manage.startswith('https://') else None
        result['account_url'] = fleet.account_url(self.config)  # the CP Account page, when linked to one (Settings, Account ↗)
        result['browser_link'] = browser_link(self.config)  # the sign-in dialog's way out to the browser itself
        result['needs_you'] = needs_you(self.config)
        result['learning_changes'] = self.learning_changes_shown(result.get('learning_changes') or [])
        by_id = {a['id']: a for a in self.config['accounts']}
        from work_or_personal import work_labels
        result['work_labels'] = work_labels(self.config)  # how each company reads on its cards: never a capitalized domain
        for area in result.get('areas') or []:  # the to-do area picker names a company the same way
            named = result['work_labels'].get(area.get('id'), '').partition(' · ')[2]
            if named and area.get('name'):
                area['label'] = area['label'].replace(area['name'], named) if area['label'] != 'Work' else 'Work'
                area['name'] = named
        result['connectors'] = [c for c in result['connectors'] if not docs_unset(c)]
        for connector in result['connectors']:
            connector.update(sign_in_help(connector.get('service', ''), connector.get('error'), result['manage_url']))
            account = by_id.get(connector['id'])
            connector.update(connector_says(account, connector.get('service', 'gmail')))
            connector.update(abilities.view(account) if account else {})
            kind = docs_provider(self.config, account)
            connector.update(reconnect_help(account, result['manage_url'], docs_offered(self.config, kind)))
            if kind == 'microsoft' and not result['manage_url'] and 'connect_name' in connector:
                connector['signin'] = fleet.SIGNIN_OF['docs']  # self-hosted: Connect Microsoft documents signs in through the control plane
            if kind and 'edit' not in (connector.get('docs_writes') or ()) and not account.get('shared') and docs_write_offered(self.config, kind):
                connector['docs_write_signin'] = 'microsoft_docs_write'  # Allow edits: Files.ReadWrite.All, its own consent
            if connector.get('service') in SIGNIN_ONLY and not result['manage_url'] and 'connect_name' in connector:
                connector['signin'] = connector['service']  # self-hosted: Reconnect is Sign in with it, through the control plane
            if result['manage_url']:
                continue  # a hosted machine: no terminal there, its account page signs in again
            if 'google_signin_expired' in (connector.get('error') or '') and connector['id'] in by_id:
                connector['sign_in_command'] = gog_signin_command(self.config, by_id[connector['id']])
            elif 'microsoft_signin_expired' in (connector.get('error') or '') and by_id.get(connector['id'], {}).get('transport') == 'graph':
                import onboarding
                connector['sign_in_command'] = 'assistant connect ' + onboarding.connect_name(by_id[connector['id']], self.config)
        result['model_usage'] = getattr(self, 'model_usage', None)
        result['model_status'] = getattr(self, 'model_status', None)
        result['chat_model'] = self.chat_model_view()
        try:  # the limit banner: a usage limit reached, which one and when it resets
            result['model_pause'] = self.model_pause()
        except Exception as error:  # noqa: BLE001 - the dashboard shows without it
            LOG.error('model pause error=%s', type(error).__name__); result['model_pause'] = None
        result['review_pause'] = self.review_pause()
        result['check'] = self.check_view()
        result['skills'] = self.skills.view() if getattr(self, 'skills', None) else None
        result['review_live'] = self.review_live()
        result['reviews_on'] = bool((self.config.get('review_worker') or {}).get('enabled'))  # off until activated
        result['reviews_auto'] = reviews_start_by_themselves(self.config)
        result['started_at'] = self.started_at()
        result['hours'] = self.hours()
        result['locale'] = self.locale_view()
        result['reminders'] = reminder_channels(self.store, self.config)  # how a snooze comes back (Telegram, notifications)
        result['todo_channels'] = reminder_channels(self.store, self.config, 'todo')  # where a to-do held for later goes (its deliver_after chip)
        result['notify'] = self.notify_view()
        result['agents_settings'] = self.agents_view()
        result['setup_hints'] = self.setup_hints_view()
        result['phone_app_store'] = phone_app_nudge(self.store)
        try:  # the setup to-do at the top of To-dos (setup_card)
            result['setup_card'] = setup_card(self.store, self.config)
        except sqlite3.Error as error:
            LOG.warning('setup card error=%s', type(error).__name__); result['setup_card'] = None
        try:  # the hello on a new owner's first views, with who has waited longest on them (Store.greeting)
            result['greeting'] = self.store.greeting(self.config.get('owner_name'))
        except sqlite3.Error as error:
            LOG.warning('greeting error=%s', type(error).__name__); result['greeting'] = None
        try:  # what the first look read and what came of it, for its ending on the list (first_look_done)
            result['first_look_done'] = self.first_look_done()
        except (sqlite3.Error, ValueError, TypeError) as error:
            LOG.warning('first look done error=%s', type(error).__name__); result['first_look_done'] = None
        try:  # the first-use tips on a new person's first to-dos (Store.first_tips)
            result['first_tips'] = self.store.first_tips()
        except sqlite3.Error as error:
            LOG.warning('first tips error=%s', type(error).__name__); result['first_tips'] = []
        result['signatures'] = self.signature_view()
        result['lookups'] = self.lookups_view()
        result['own_addresses'] = self.own_addresses_view()
        result['team_learnings'] = self.learnings_view()
        result['security'] = self.security_view()
        self.heartbeat_health(result['review_health'])
        for suggestion in result.get('suggestions', []):
            suggestion['snooze_choices'] = snooze_choices(self.is_work(suggestion.get('account_ids')))
        if getattr(self, 'agents', None):
            try:
                result['agent_tools'] = self.agents.tools()
                with self.store.connect() as db:
                    self.agents.annotate(db, result.get('suggestions', []))
            except (sqlite3.Error, ValueError) as error:
                LOG.error('agent jobs status error=%s', type(error).__name__)
        if getattr(self, 'fleet', None):
            try:
                result['fleet'] = {**self.fleet.summary(), 'family_invites': self.fleet.family_invite_on()}
                with self.store.connect() as db:
                    self.fleet.annotate(db, result.get('suggestions', []))
                    self.fleet.family_invite_annotate(db, result.get('suggestions', []))
            except (sqlite3.Error, ValueError) as error:
                LOG.error('fleet status error=%s', type(error).__name__)
        try:
            with self.store.connect() as db:
                self.task_pages.annotate(db, result.get('suggestions', []))
                self.handoff_mail.annotate(db, result.get('suggestions', []))
            if isinstance(result.get('fleet'), dict):
                result['fleet']['take_line'] = self.handoff_mail.take_line()
        except (sqlite3.Error, ValueError) as error:
            LOG.error('task pages status error=%s', type(error).__name__)
        return result

    def agent_status(self, suggestion_id=None):
        """The agent's compact status, built from a lean snapshot without the dashboard's views: the whole status took
        longer than the tool's 30 seconds on a busy Machine, while an agent reads only this. suggestion_id: only that
        to-do and the decisions on it (card_status)."""
        result = self.store.snapshot(self.config['accounts'], lean=True)
        if suggestion_id and not any(s.get('id') == suggestion_id for s in result['suggestions']):
            try:  # an older done to-do, past the last 100 the snapshot keeps
                with self.store.connect() as db:
                    row = db.execute('SELECT * FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
                    if row:
                        result['suggestions'].append(dict(row))
                        self.store.card_views(db, result['suggestions'][-1:], jobs=False)
            except (sqlite3.Error, ValueError) as error:
                LOG.error('card status error=%s', type(error).__name__)
        result['connectors'] = [c for c in result['connectors'] if not docs_unset(c)]
        self.heartbeat_health(result['review_health'])
        if getattr(self, 'agents', None):
            try:
                with self.store.connect() as db:
                    self.agents.annotate(db, result.get('suggestions', []))
            except (sqlite3.Error, ValueError) as error:
                LOG.error('agent jobs status error=%s', type(error).__name__)
        return card_status(result, suggestion_id) if suggestion_id else compact_status(result)
