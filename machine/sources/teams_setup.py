"""Microsoft Teams' setup checks for onboarding.py (connectors/teams.py reads it): whether + Add offers it, and what
its account still needs before it can read."""
import types


def offered(config):
    """Teams signs in through the hosted Machine's Microsoft consent: offered once that offers it (teams_consent)."""
    return bool(config.get('teams_consent'))


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
