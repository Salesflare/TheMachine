"""Settings, Notifications, Weekly recap: the owner's switch for the recap (App.recap_step sends it). It is the
`weekly_recap` setting in config.json (enabled, weekday, at), saved there like Work hours, so a hosted Machine turns it
on from the dashboard too. On by default: the switch stores the owner's choice with `chosen`, so only an owner who
turned it off has it off. An `enabled: false` without `chosen` is what every install wrote before (config.example.json)
and is no choice, so it reads as on. A mixin of assistant.App (APP_MIXINS)."""
from machine.app.card_chat import save_hours  # config.json's careful write (a .bak, then an atomic replace)

RECAP_DEFAULT = {'enabled': True, 'weekday': 5, 'at': '16:00'}


def recap_settings(config):
    """`weekly_recap` as the recap reads it: its defaults, then config.json's own values. `enabled` counts only when
    the owner chose it (`chosen`, the switch); otherwise it is the default, on."""
    own = config.get('weekly_recap') if isinstance(config.get('weekly_recap'), dict) else {}
    settings = {**RECAP_DEFAULT, **own}
    if not own.get('chosen'):
        settings['enabled'] = RECAP_DEFAULT['enabled']
    return settings


class RecapSettingsApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'recap_set': 'recap_set_action'}

    def recap_switch_view(self):
        """The switch's state: on or off, the day (1 Monday to 7 Sunday) and time it comes, and whether it can be saved."""
        settings = recap_settings(self.config)
        return {'on': bool(settings['enabled']), 'weekday': settings['weekday'], 'at': settings['at'],
                'saveable': bool(getattr(self, 'config_path', None))}

    def recap_set_action(self, name, args, owner_dashboard):
        """The owner turns the weekly recap on or off in Settings: saved in config.json as their choice (other keys and
        its day and time kept) and in use at once; recap_step reads it on its next round."""
        if not owner_dashboard:
            raise ValueError('Only the owner turns the weekly recap on or off, in Settings')
        if not getattr(self, 'config_path', None):
            raise ValueError('This can’t be changed on this Machine.')
        value = {**recap_settings(self.config), 'enabled': args.get('on') is True, 'chosen': True}
        save_hours(self.config_path, {'weekly_recap': value})
        self.config['weekly_recap'] = value
        return self.recap_switch_view()
