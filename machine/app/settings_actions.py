"""The dashboard's Settings actions (App.action): own addresses and domains, Look up work contacts, agents, tips,
region, work hours, security levels, how the owner writes, a connector's sync and model usage. Moved out of
assistant.App's action as is. A mixin of assistant.App (APP_MIXINS)."""
import re

import enrichment
from machine.config import LOG
from machine.model_usage import usage_status, use_model_reset
import own_addresses
import security_levels
from timeutil import now


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
