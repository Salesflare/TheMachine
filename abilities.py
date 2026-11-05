"""A connection's two abilities: Brings in signals, and Can do things (docs/help/connections.md, Abilities).

- signals: it syncs. What comes in (mail, chats, events, doc comments) is read, reviewed and becomes to-dos.
- actions: the Machine may use it for a to-do: reads on demand (a doc's text, a search for a doc), and drafts that go
  out or change something (an email, a reply, a calendar change, a doc), each still only after the owner's OK.

A connection has the abilities its kind allows (capable): every one brings in signals; one that can send, reply, change
events or work with docs can also do things, unless a Fleet shares it (someone else's sign-in only reads). One with both
gets a switch for each on its card (switchable), at least one of them on (both off is Disconnect). A chat's or
Intercom's replies answer what came in, so there only Can do things has a switch. Off is stored on the account
as "signals": false or "actions": false in config.json; a key that isn't there is on, so every connection from before
keeps what it did (no migration step). A connection with signals off is action-only: no sync runs, and its card shows no
sync counts."""
from __future__ import annotations

SIGNALS, ACTIONS = 'signals', 'actions'
ABILITIES = (SIGNALS, ACTIONS)
REPLY_SERVICES = ('slack', 'whatsapp', 'telegram', 'linkedin', 'x')


def can_act(account):
    """Whether this kind of connection can do things at all (switch or not): send mail, reply in a chat, change a
    calendar, or work with docs. Never one a Fleet shares."""
    import calendar_writes  # noqa: PLC0415 - next_actions and calendar_writes import this module's callers
    import next_actions  # noqa: PLC0415
    if not isinstance(account, dict) or account.get('shared'):
        return False
    service = account.get('service', 'gmail')
    return bool(next_actions.mail_account(account) or calendar_writes.writable(account) or service in REPLY_SERVICES
                or service == 'docs' or service == 'intercom' and next_actions.intercom_replies_on(account))


def switchable(account):
    """The abilities the owner can turn off on this connection's card: none with one ability; with both, both, except
    where its actions answer what it brings in (chat and Intercom replies), which keep signals on."""
    has = capable(account)
    if len(has) < 2:
        return []
    service = account.get('service', 'gmail')
    return [ACTIONS] if service in REPLY_SERVICES or service == 'intercom' else list(ABILITIES)


def capable(account):
    """The abilities this connection's kind has: signals always, actions where it can act."""
    return {SIGNALS, *([ACTIONS] if can_act(account) else [])}


def on(account, ability):
    """Whether the owner left this ability on: off only as an explicit false (a connection from before is on)."""
    return isinstance(account, dict) and ability in capable(account) and account.get(ability) is not False


def signals_on(account):
    """It syncs. Not capability-checked: every connection can bring in signals."""
    return isinstance(account, dict) and account.get(SIGNALS) is not False


def actions_on(account):
    return on(account, ACTIONS)


def view(account):
    """The card's abilities: which it has, which are on, and whether it gets switches (only with both)."""
    has = capable(account)
    return {'abilities': [a for a in ABILITIES if a in has], 'signals': signals_on(account),
            'actions': ACTIONS in has and actions_on(account), 'ability_switches': switchable(account)}


def check(account, values):
    """The owner's switches for this account, checked: {signals: bool, actions: bool}, both of the abilities it has,
    at least one on. Returns the account's new fields (False where off, None to drop the key: on). Raises ValueError."""
    switches = switchable(account)
    if not switches:
        raise ValueError('This connection has one ability. To stop it, disconnect it.')
    if not isinstance(values, dict) or set(values) != set(ABILITIES) or not all(isinstance(values[a], bool) for a in ABILITIES):
        raise ValueError('Give signals and actions, each on or off')
    if not any(values.values()):
        raise ValueError('Keep one on. To stop it, disconnect it.')
    if any(not values[a] for a in ABILITIES if a not in switches):
        raise ValueError('Its replies answer what it brings in, so Brings in signals stays on')
    return {a: None if values[a] else False for a in ABILITIES}


def refuse(config, account_id):
    """Why the Machine may not do things with this account (its Can do things is off), else None."""
    account = next((a for a in (config or {}).get('accounts') or () if a.get('id') == account_id), None)
    if account is None or not can_act(account) or actions_on(account):
        return None
    import i18n  # noqa: PLC0415
    return i18n.t('Can do things is off for {}. Turn it on under Connections first.',
                  str(account.get('display_name') or account.get('email') or account_id))
