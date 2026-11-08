"""The dashboard's Settings actions (App.action): own addresses and domains, Look up work contacts, agents, tips,
region, work hours, security levels, how the owner writes, a connector's sync and model usage. Moved out of
assistant.App's action as is. A mixin of assistant.App (APP_MIXINS)."""
import json
import re
import sqlite3
import time
from zoneinfo import ZoneInfo

import activity
import activity_log
import agent_jobs
import enrichment
import error_feed
import fleet
import help_topics
import locale_prefs
from machine.app.card_chat import save_hours
from machine.config import LOG
from machine.delivery.push import setup_hints
from machine.model_usage import telegram_on, usage_status, use_model_reset
import own_addresses
import security_levels
import team_learnings
from timeutil import clock, local_tz, now, set_timezone, set_work_hours, WORK_HOURS, work_hours, WORK_HOURS_DEFAULT


def hours_settings(config, changes):
    """`timezone`, `digest_at` and `work_hours` after `changes` (any of those, or the work_hours keys
    days/start/end/morning at the top level), checked; a ValueError says what is wrong."""
    current = {**WORK_HOURS_DEFAULT, **(config.get('work_hours') or {})}
    nested = changes.get('work_hours') if isinstance(changes.get('work_hours'), dict) else {}
    merged = {**current, **nested, **{k: changes[k] for k in WORK_HOURS_DEFAULT if changes.get(k) is not None}}
    zone = str(changes.get('timezone') or config.get('timezone') or getattr(local_tz(), 'key', '') or 'UTC').strip()
    try:
        ZoneInfo(zone)
    except (ValueError, KeyError, OSError):
        raise ValueError(f'Unknown time zone {zone!r}; use a name like Europe/Brussels or America/New_York') from None
    digest = '%02d:%02d' % clock(changes.get('digest_at') or config.get('digest_at') or '08:30', 'The digest time')
    return {'timezone': zone, 'digest_at': digest, 'work_hours': work_hours(merged)}


def activity_report(db, timezone=None, current=None):
    """Per local day, the last 7 days: plain counts of what the owner did (to-dos shown and opened, Do it, Send,
    sent, Mark done, Not needed, snoozed, chat messages, visits, active hours), for the hosted health report next to
    first_cards_report. Counts only, never content (activity.py). `db`: a plain sqlite3 connection to the events database."""
    try:
        tz = ZoneInfo(timezone) if timezone else local_tz()
    except (ValueError, KeyError):
        tz = local_tz()
    return activity.report(db, tz, current or now())


class SettingsActionsApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'set_voice': 'set_voice_action', 'security_level': 'security_action',
               'security_setting': 'security_action', 'own_address': 'own_address_action',
               'own_domain': 'own_domain_action', 'set_people_lookup': 'set_people_lookup_action',
               'set_agents': 'set_agents_action', 'tip_done': 'tip_done_action', 'set_locale': 'set_locale_action',
               'connector_sync': 'connector_sync_action', 'set_work_hours': 'set_work_hours_action',
               'model_usage_refresh': 'model_usage_action', 'model_reset': 'model_usage_action'}

    def set_voice_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner edits how they write, in Settings')
        self.store.save_voice(args.get('channel'), args.get('text'), 'owner')
        return {'voices': self.store.voices()}

    def security_action(self, name, args, owner_dashboard=False):
        # Settings, Security (security_levels.py)
        if not owner_dashboard:
            raise ValueError('Only the owner changes security settings, in Settings on the dashboard')
        with self.store.connect() as db:
            if name == 'security_level':
                rules = security_levels.apply(db, str(args.get('level') or ''))
            else:
                rules = []
                security_levels.set_pref(db, str(args.get('key') or ''), str(args.get('value') or ''))
        for ref, kind, rule in rules:
            if ref and self.fleet:
                self.fleet.set_rule(ref, security_levels.ALL, kind, rule)
        if name == 'security_level' and self.fleet:  # the Network switches follow the level now, not on the next round
            try:
                self.fleet.network_defaults()
            except Exception as error:  # noqa: BLE001 - the next Network round sets them
                LOG.info('network defaults after a level change failed error=%s', type(error).__name__)
        return {'security': self.security_view(), 'lookups': self.lookups_view(), 'team_learnings': self.learnings_view()}

    def own_address_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner confirms or removes their addresses, in Settings')
        with self.store.connect() as db:
            own_addresses.choose(db, args.get('address'), str(args.get('choice') or ''), now(), self.config)
        self.graph_dirty.set()  # who counts as the owner changed: the graph follows within a minute
        return {'own_addresses': self.own_addresses_view()}

    def own_domain_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner changes their company’s domains, in Settings')
        with self.store.connect() as db:
            own_addresses.set_domain(db, args.get('domain'), args.get('on') is not False, now(), self.config)
        self.graph_dirty.set()  # its people become colleagues and its organization folds into the owner's: within a minute
        return {'own_addresses': self.own_addresses_view()}

    def set_people_lookup_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner turns Look up work contacts on or off, in Settings')
        with self.store.connect() as db:
            enrichment.set_people(db, args.get('on') is not False)
        return self.lookups_view()

    def set_agents_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner changes this, on the dashboard (Settings)')
        return self.set_agents(args)

    def tip_done_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner closes a tip, on the dashboard')
        return self.store.tip_done(args.get('tip'))

    def set_locale_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner changes region and time format, on the dashboard (Settings, General)')
        return self.set_locale(args)

    def connector_sync_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner stops or restarts a sync, on the dashboard (Connections)')
        return self.connector_sync(args)

    def set_work_hours_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner changes work hours, on the dashboard or with: assistant hours')
        return self.set_hours(args)

    def model_usage_action(self, name, args, owner_dashboard=False):
        if not owner_dashboard:
            raise ValueError('Only the owner can do this, on the dashboard')
        if name == 'model_reset':
            reply = getattr(self, 'model_usage_reply', None) or usage_status(self.config)
            key = str(args.get('key') or '')
            if not re.fullmatch(r'[A-Za-z0-9-]{8,80}', key):
                raise ValueError('Invalid request')
            outcome = use_model_reset(self.config, reply, key)
            LOG.info('model usage reset outcome=%s', outcome)
        self.refresh_model_usage()
        status = getattr(self, 'model_status', None)
        return {'model_status': status, 'model_usage': getattr(self, 'model_usage', None),
                **({'outcome': outcome} if name == 'model_reset' else {})}

    def hours(self):
        """Work hours as the dashboard shows and edits them."""
        return {**WORK_HOURS, 'timezone': getattr(local_tz(), 'key', str(local_tz())), 'digest_at': self.config.get('digest_at', '08:30'),
                'saveable': bool(getattr(self, 'config_path', None))}

    def set_hours(self, args):
        """The owner's Work hours from the dashboard: checked, saved in config.json and in use at once."""
        if not getattr(self, 'config_path', None):
            raise ValueError('This can’t be changed on this Machine.')
        values = hours_settings(self.config, args)
        save_hours(self.config_path, values)
        self.config.update(values)
        set_timezone(values['timezone'])
        set_work_hours(values['work_hours'])
        return self.hours()

    def locale_view(self):
        """Language and region as Settings shows them and the dashboard formats dates and times (locale_prefs)."""
        return {**locale_prefs.view(), 'saveable': bool(getattr(self, 'config_path', None))}

    def set_locale(self, args):
        """The owner's language, region, time format and To-dos filter from the dashboard: checked, saved in config.json and in use at once."""
        if not getattr(self, 'config_path', None):
            raise ValueError('This can’t be changed on this Machine.')
        if 'browser' in args:  # the dashboard's first load on a Machine without a region: the browser's, never over a choice
            browser = args['browser'] if isinstance(args['browser'], dict) else {}
            found = locale_prefs.guess(browser.get('zone'), browser.get('language'))
            if self.config.get('locale') or not found:
                return self.locale_view()
            args = {'locale': found}
        values = locale_prefs.settings(args)
        save_hours(self.config_path, values)
        self.config.update(values)
        locale_prefs.configure(self.config)
        return self.locale_view()

    def setup_hints_view(self):
        """setup_hints, worked out at most every 10 minutes: the dashboard asks for its state every few seconds."""
        # a source, Telegram or Codex connected just now drops its hint at once
        key = (tuple(sorted(str(a.get('service')) for a in self.config.get('accounts') or [] if isinstance(a, dict))),
               telegram_on(self.config), json.dumps(self.config.get('agents'), sort_keys=True, default=str))
        cached = getattr(self, '_setup_hints', None)
        if cached and cached[1] == key and time.monotonic() - cached[0] < 600:
            return cached[2]
        try:
            hints = setup_hints(self.store, self.config)
        except (sqlite3.Error, OSError, ValueError):
            hints = []
        self._setup_hints = (time.monotonic(), key, hints)
        return hints

    def set_agents(self, args):
        import agent_remote
        if not getattr(self, 'config_path', None):
            raise ValueError('This can’t be changed on this Machine.')
        session = str(args.get('claude_session') or '').strip()
        found = agent_remote.session_id(session) if session else ''
        if session and not found:
            raise ValueError('Paste the session link from claude.ai/code')
        env, branch = str(args.get('codex_env') or '').strip(), str(args.get('codex_branch') or '').strip()
        if env and not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', env):
            raise ValueError('That is not a Codex environment id')
        if branch and not re.fullmatch(r'[A-Za-z0-9._/-]{1,120}', branch):
            raise ValueError('That is not a branch name')
        own = dict(agent_jobs.settings(self.config) or {})
        claude = {k: v for k, v in (own.get('claude') if isinstance(own.get('claude'), dict) else {}).items() if k not in ('session', 'device')}
        codex = {k: v for k, v in (own.get('codex') if isinstance(own.get('codex'), dict) else {}).items() if k not in ('env', 'branch')}
        if found:
            claude.update(place='remote', session=found, **({'device': str(args['device']).strip()[:60]} if str(args.get('device') or '').strip() else {}))
        if env:
            codex.update(place='cloud', env=env, **({'branch': branch} if branch else {}))
        for part, key, place in ((claude, 'session', 'remote'), (codex, 'env', 'cloud')):
            if not part.get(key) and part.get('place') == place:
                part.pop('place')
        own.update(claude=claude, codex=codex)
        save_hours(self.config_path, {'agents': own})
        self.config['agents'] = own
        return self.agents_view()

    def account_view(self):
        """Settings, Account on a self-hosted Machine paired with the Network: its owner's account in short, from the
        control plane (fleet.Fleet.account). A hosted Machine's dashboard asks the control plane itself, with the owner's
        sign-in on that host (/_machine/account), so this Machine never holds what opens the account's pages."""
        if not getattr(self, 'fleet', None):
            return {'on': False}
        try:
            return {'on': True, **self.fleet.account()}
        except (fleet.Off, ValueError, OSError) as error:
            LOG.info('account summary unavailable error=%s', type(error).__name__)
            return {'on': True, 'error': 'Can’t reach your account right now.'}

    def security_view(self):
        """Settings, Security: the owner's level (Standard, Careful or Custom) and each Work Fleet's."""
        try:
            with self.store.connect() as db:
                return security_levels.view(db)
        except sqlite3.Error:
            return None

    def learnings_view(self):
        """Feedback, Share learnings with The Machine team, and its Settings switch (team_learnings.py)."""
        try:
            with self.store.connect() as db:
                # and Share what Help is asked (help_topics.py) and Send error reports (error_feed.py), on the same Settings card
                return {**team_learnings.view(db, network=bool(getattr(self, 'fleet', None))), 'help_topics': help_topics.on(db), 'errors': error_feed.on(db)}
        except sqlite3.Error:
            return None

    def activity_view(self, kind='', cursor=0, outcome='', actor=''):
        """Settings, Activity: one page of everything The Machine did, newest first (activity_log.page). Read-only."""
        self.note_connections()
        with self.store.connect() as db:
            return activity_log.page(db, self.config, kind, cursor, outcome=outcome, actor=actor)

    def note_connections(self):
        """Activity: remember the connections there are now, so one added or removed since shows (activity_log.py).
        Never stops the service: a failed note only costs that line."""
        try:
            with self.store.connect() as db:
                activity_log.note_accounts(db, self.config.get('accounts') or [], now())
        except sqlite3.Error as error:
            LOG.warning('activity connections not noted error=%s', type(error).__name__)
