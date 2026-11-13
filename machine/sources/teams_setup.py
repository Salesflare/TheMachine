"""Microsoft Teams' setup checks for onboarding.py (connectors/teams.py reads it): whether + Add offers it, and what
its account still needs before it can read."""
import types


def offered(config):
    """Teams signs in through The Machine's Microsoft consent: on a hosted Machine once its account page offers it
    (teams_consent); on a self-hosted one once it is paired with an account, which starts it from + Add (fleet.py
    connect_start, microsoft_teams; the dashboard leaves it out while the control plane doesn't open that sign-in)."""
    if config.get('teams_consent'):
        return True
    return not config.get('manage_url') and bool((config.get('credentials') or {}).get('fleet'))


def missing(config, account, plugin, error):
    """What the Teams account still needs, or '': its address, the broker, and a Microsoft sign-in for that address
    (Outlook's, or its own). plugin: onboarding's connector loader; error: the SetupError its sign-in raises."""
    if not account.get('email'):
        return 'email is not set'
    if account.get('transport') == 'broker' and not (config.get('microsoft_broker') or {}).get('url'):
        return 'microsoft_broker url is not set'
    teams = plugin('teams')
    try:
        teams and teams.signin(config, account, types.SimpleNamespace(SourceError=error))
    except error:
        return 'no Microsoft sign-in for this address yet'
    return ''
