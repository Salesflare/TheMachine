"""Setting up any other mailbox over IMAP (imap_mail.py): the + Add form asks the address and password; its Server
settings, folded away, fill in or change what imap_presets.py finds (onboarding.web_form shows FIELDS). The
password is checked by signing in before anything is saved, to the IMAP server and to the SMTP server it sends through
(smtp_mail.py): a mailbox whose SMTP server refuses still connects, and only reads. Moved out of onboarding.py (its line budget). onboarding
imports this module, so this one imports onboarding where it is used."""
import re
from pathlib import Path

import imap_mail
import imap_presets
import smtp_mail

ACCOUNT = {'id': 'work-imap', 'service': 'imap', 'transport': 'imap', 'boundary': 'work:Acme'}
FIELDS = [['username', 'Username'],  # its own row; then one row per server (dashboard/connections-cards.js)
          ['imap_host', 'IMAP server'], ['imap_port', 'IMAP port'], ['imap_security', 'IMAP security', ['SSL/TLS', 'STARTTLS']],
          ['smtp_host', 'SMTP server'], ['smtp_port', 'SMTP port'], ['smtp_security', 'SMTP security', ['SSL/TLS', 'STARTTLS']]]
STARTTLS_PORTS = (25, 143, 587, 1025, 1143, 2525)
IDENTITY = {'sent_folder', 'imap_host', 'imap_port', 'imap_security', 'username', 'smtp_host', 'smtp_port',
            'smtp_security', 'smtp_refused'}  # a mailbox's own server settings: never copied to another one (onboarding.new_account)
HINTS = (  # onboarding.hint: what to do about a sync error
    ('imap_auth_failed', 'the mail server refused the password: connect it again (many providers need an app password)'),
    ('imap_tls_failed', 'no secure connection to the mail server: check its name, port and security'),
    ('imap_unreachable', 'could not reach the mail server; it retries by itself (check its name if it keeps failing)'),
    ('imap_password_missing', 'the mailbox has no saved password: connect it again'),
    ('imap', 'the mail server did not answer as expected; it retries by itself'),
)


def given(ui, prompt):
    """What the dashboard's form answered to this prompt (onboarding.WebUI.prefill), without asking; None when it left
    it, and always None in a terminal."""
    import onboarding  # noqa: PLC0415 - onboarding imports this module
    key = onboarding._prompt_key(prompt)
    return next((v for k, v in (getattr(ui, 'answers', None) or {}).items() if onboarding._prompt_key(k) in key and v), None)


def tls_mode(text, port):
    """SSL/TLS or STARTTLS as typed: 'ssl' or 'starttls'. A bare "TLS" on a submission port (587) is STARTTLS, as
    providers' help pages write it. Anything without TLS is refused."""
    import onboarding  # noqa: PLC0415 - onboarding imports this module
    value = re.sub(r'[^a-z]', '', str(text or '').lower())
    if value in ('ssl', 'ssltls', 'implicittls', 'implicit'):
        return 'ssl'
    if value in ('starttls', 'tlsstarttls'):
        return 'starttls'
    if value == 'tls':
        return 'starttls' if port in STARTTLS_PORTS else 'ssl'
    raise onboarding.SetupError('The Machine only connects to mail servers over TLS', 'pick SSL/TLS or STARTTLS in Server settings')


def port_number(text, default):
    import onboarding  # noqa: PLC0415 - onboarding imports this module
    value = str(text or '').strip() or str(default)
    if not value.isdigit() or not 0 < int(value) < 65536:
        raise onboarding.SetupError('That port is not a number from 1 to 65535', 'check the ports in Server settings')
    return int(value)


REFUSED = {
    'imap_auth_failed': 'The mail server refused the email address or password',
    'imap_tls_failed': 'Couldn’t make a secure connection to the mail server',
    'imap_unreachable': 'Couldn’t reach the mail server',
    'timeout': 'The mail server didn’t answer in time',
    'imap_rate_limited': 'The mail server asked to slow down',
    'imap_unavailable': 'The mail server is busy',
    'imap_no_inbox': 'The mail server has no inbox for this account',
}


def step(config, account, ui):
    """Any other mailbox over IMAP: the address, its server settings (found for it, or as typed in Server settings) and
    its password, checked by logging in before anything is saved. Gmail and Microsoft mail are steered to their own
    connection, which needs no password. Signing in again asks only for the password."""
    import onboarding  # noqa: PLC0415 - onboarding imports this module
    again = bool(account.get('email')) and getattr(ui, 'reconnect', False)
    if not again:
        email = ui.ask('Email address', account.get('email') or '').strip().lower()
        if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', email):
            raise onboarding.SetupError('No email address given', 'fill in your email address')
        account['email'] = email
        typed = given(ui, 'IMAP server')
        found = {} if typed else imap_presets.lookup(email)
        if found.get('oauth'):
            gmail = found['oauth'] == 'gmail'
            raise onboarding.SetupError(f"{email} signs in with {'Google' if gmail else 'Microsoft'}",
                             f"add {'Gmail' if gmail else 'Outlook'} instead: it needs no password")
        if found.get('name'):
            ui.say(f"  {found['name']} settings found")
        host = ui.ask('IMAP server', found.get('imap_host') or '').strip().lower()
        if not host or not re.fullmatch(r'[a-z0-9.:\[\]-]+', host):
            raise onboarding.SetupError('No IMAP server given', 'fill in Server settings with what your provider gives for mail apps')
        security = tls_mode(ui.ask('IMAP security', {'ssl': 'SSL/TLS', 'starttls': 'STARTTLS'}.get(found.get('imap_security'), 'SSL/TLS')),
                                 int(found.get('imap_port') or 993))
        port = port_number(ui.ask('IMAP port', str(found.get('imap_port') or (993 if security == 'ssl' else 143))), 993)
        if security == 'ssl' and port in STARTTLS_PORTS and not found:
            security = 'starttls'  # SSL/TLS left as it was, with a STARTTLS port typed: that port's way
        smtp_guess = found.get('smtp_host') or (re.sub(r'^imap\.', 'smtp.', host) if host.startswith('imap.') else host)
        smtp_security = tls_mode(ui.ask('SMTP security', {'ssl': 'SSL/TLS', 'starttls': 'STARTTLS'}.get(found.get('smtp_security'), 'STARTTLS')),
                                      int(found.get('smtp_port') or 587))
        account.update(imap_host=host, imap_port=port, imap_security=security,
                       username=ui.ask('Username', found.get('username') or email).strip() or email,
                       smtp_host=ui.ask('SMTP server', smtp_guess).strip().lower() or smtp_guess,
                       smtp_security=smtp_security,
                       smtp_port=port_number(ui.ask('SMTP port', str(found.get('smtp_port') or (465 if smtp_security == 'ssl' else 587))), 587))
    account['credential'] = 'imap-' + account['id']
    path = Path(config.setdefault('credentials', {}).setdefault(account['credential'], str(onboarding.data_dir(config) / f"imap-{account['id']}"))).expanduser()
    has = path.exists() and bool(path.read_text().strip())
    password = ui.secret('Password' + (' (Enter keeps the saved one)' if has else ''))
    if not password and has:
        password = path.read_text().strip()
    if not password:
        raise onboarding.SetupError('No password given', 'fill in the password for this mailbox')
    try:
        sent = imap_mail.check(config, lambda _config, _name: password, account)  # before anything is saved
    except imap_mail.ImapError as error:
        what = REFUSED.get(error.category, 'The mail server didn’t answer as expected')
        found = imap_presets.builtin(account['email']) or {}
        if error.category == 'imap_auth_failed':
            fix = ('use the password Proton Mail Bridge shows' if found.get('password') == 'bridge'
                   else f"use your {found['name']} mail password" if found.get('password') == 'mail'
                   else 'use an app password: ' + found['help'] if found.get('help')
                   else 'check the password; many providers need an app password for mail apps')
        else:
            fix = 'check the server name, port and security in Server settings'
        raise onboarding.SetupError(what, fix) from None
    try:
        smtp_mail.check(config, None, account, password)
        account.pop('smtp_refused', None)
    except smtp_mail.SmtpError as error:
        account['smtp_refused'] = True  # reads; sending waits for a sign-in the SMTP server takes
        ui.say(f"  sending: {REFUSED.get(error.category.replace('smtp_', 'imap_'), 'the mail server for sending didn’t answer as expected')}: reading only")
    if sent:
        account['sent_folder'] = sent
    else:
        account.pop('sent_folder', None)
        ui.say('  no Sent folder found: reading the inbox only')
    onboarding.write_private(path, password + '\n')
    ui.say('  signed in')
