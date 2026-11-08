"""Gmail and Google Calendar from one Google sign-in.

The own-app sign-in asks Google for both, read-only (onboarding's sign_in), so connecting one adds the other too: the
same address, the same Google app and the same part of the owner's life, with no second sign-in. The dashboard,
`assistant connect` and the installer all connect through here. Nothing more is ever asked of Google.

`ob` is the onboarding module its caller already loaded (cli.py loads its own copy from the file)."""
import json

PAIR = {'gmail': 'calendar', 'calendar': 'gmail'}


def connect(ob, config_path, name, ui, account_id=None, restart=True):
    """onboarding.connect, then the other one of the pair when the same sign-in holds it. Returns the account picked;
    the other one never stops it: one that does not work is left out, and the one picked stays connected."""
    account = ob.connect(config_path, name, ui, account_id, restart=False)
    config = ob.load(config_path)
    sibling = also(ob, config, account, ui)
    if sibling:
        config['accounts'] = config.get('accounts', []) + [sibling]
        ob.save(config_path, config)
    if restart:
        ob.restart_and_sync(config, [a['id'] for a in (account, sibling) if a], ui, config_path=config_path)
    return account


def also(ob, config, account, ui):
    """The other one of the pair, ready to save, or None: not a Google source through gog, already connected for that
    address, not held by gog's sign-in, or not working yet."""
    other, email = PAIR.get(account.get('service')), str(account.get('email') or '').lower()
    if not other or account.get('transport') != 'gog' or not config.get('gog') or not email:
        return None
    if any(a.get('service') == other and str(a.get('email') or '').lower() == email for a in config.get('accounts', [])):
        return None
    listed = ob.run([config['gog'], 'auth', 'list', '--json', '--no-input'], env=ob.gog_env(config), timeout=30)
    try:
        entry = next(a for a in json.loads(listed.stdout).get('accounts', []) if str(a.get('email', '')).lower() == email
                     and (a.get('client') or 'default') == account.get('client', 'default'))
    except (ValueError, AttributeError, TypeError, StopIteration):
        return None
    if other not in [str(s) for s in entry.get('services') or []]:
        return None
    sibling = ob.new_account(config, other, ui=ob.AnswersUI({'part of your life': account.get('boundary')}))
    sibling.update({k: account[k] for k in ('email', 'client', 'boundary', 'boundary_by') if k in account}, transport='gog')
    if other == 'calendar':
        sibling.setdefault('calendar_id', 'primary')
    error = ob.check(config, sibling)
    if error and not error.startswith(ob.BUSY):
        if other == 'calendar':
            ui.say('Google Calendar isn’t connected yet. Add it under + Add.')
        return None
    ui.say(f'  ✓ {ob.label(other)} connected')
    return sibling
