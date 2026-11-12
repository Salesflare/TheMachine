"""Setting up any other mailbox over IMAP (imap_mail.py): the + Add form asks the address and password; its Server
settings, folded away, fill in or change what imap_presets.py finds (onboarding.web_form shows FIELDS). The
password is checked by signing in before anything is saved, to the IMAP server and to the SMTP server it sends through
(smtp_mail.py): a mailbox whose SMTP server refuses still connects, and only reads. Moved out of onboarding.py (its line budget). onboarding
imports this module, so this one imports onboarding where it is used."""
import re
import socket
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
            'smtp_security', 'smtp_refused', 'tls_pin', 'smtp_tls_pin'}  # a mailbox's own server settings: never copied to another one (onboarding.new_account)
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


def steer(email, oauth):
    """Gmail and Microsoft mail, found for the address or typed as its server, go to their own connection: Microsoft
    has turned off password sign-in for mail apps, and Google's own connection needs no app password."""
    import onboarding  # noqa: PLC0415 - onboarding imports this module
    if oauth:
        gmail = oauth == 'gmail'
        raise onboarding.SetupError(f"{email} signs in with {'Google' if gmail else 'Microsoft'}",
                                    f"add {'Gmail' if gmail else 'Outlook'} instead: it needs no password")


def hosted(config):
    from machine.sources import gateway  # noqa: PLC0415 - only here
    return gateway.hosted(config)


def pin(account, ui):
    """A mail server on this computer (Proton Mail Bridge) has its own self-signed certificate: the one it shows now
    is pinned, and only that one is trusted from then on (imap_mail.check_pin). The owner sees its fingerprint, the
    one in the certificate Bridge exports (Settings, Advanced, Export TLS certificates)."""
    for key, kind in (('tls_pin', 'imap'), ('smtp_tls_pin', 'smtp')):
        host = account.get(f'{kind}_host')
        account.pop(key, None)
        if host not in imap_mail.LOOPBACK:
            continue
        found = imap_mail.peer_certificate(host, int(account.get(f'{kind}_port') or 0), account.get(f'{kind}_security'), kind, verify=False)
        if found:
            account[key] = imap_mail.fingerprint(found[0])
            if kind == 'imap' or account[key] != account.get('tls_pin'):
                ui.say(f'  trusting only this certificate of the mail server on this computer: SHA-256 {account[key]}')


def wrong_name(account, kind):
    """(the name to use, the name typed) when the server's certificate is trusted but made out to another name, as on
    shared hosting (mail.your-domain answered by the host's own server) or a server typed as its IP address."""
    host = account.get(f'{kind}_host')
    if host in imap_mail.LOOPBACK:
        return None
    found = imap_mail.peer_certificate(host, int(account.get(f'{kind}_port') or 0), account.get(f'{kind}_security'), kind)
    use = name_to_use(found[1], host, kind) if found else None
    return (use, host) if use else None


def covers(name, host):
    """Whether a certificate name (maybe a wildcard, *.example.com) covers this host, as TLS checks it."""
    name = name.lower()
    if name.startswith('*.'):
        return host.count('.') == name.count('.') and host.endswith(name[1:])
    return host == name


def resolves(host):
    try:
        return bool(socket.getaddrinfo(host, None))
    except (OSError, UnicodeError):
        return False


def name_to_use(names, typed, kind='imap'):
    """The server name a certificate is for, to use instead of the one typed: a provider's mail server we know that it
    covers (imap.ionos.com), else its own name for this protocol (imap. or smtp.), a mail server's (mail.), a server's
    (am12.host.example), a wildcard's mail name that exists (*.host.example: mail.host.example), the domain. None when
    it names nothing usable."""
    known = imap_presets.known_hosts(kind)
    hit = next((h for h in known for n in names if covers(n, h)), None)
    if hit:
        return hit
    plain = [n.lower() for n in names if '*' not in n and n.lower() != typed]
    own = [n for n in plain if n.split('.')[0].rstrip('s') == kind]
    mail = [n for n in plain if n.split('.')[0] in ('mail', 'ssl0', 'secure')]
    servers = [n for n in plain if n.count('.') >= 2]
    first = typed.split('.')[0] if re.search('[a-z]', typed) else None
    stars = [f'{label}{n[1:].lower()}' for n in names if n.startswith('*.') for label in (first, kind, 'mail') if label]
    return next((n for n in own + mail + servers if n), None) or next((n for n in stars if resolves(n)), None) \
        or (plain or [None])[0]


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
        steer(email, found.get('oauth'))
        if found.get('name'):
            ui.say(f"  {found['name']} settings found")
        if found.get('help'):
            ui.say(f"  {found['name']} needs an app password for mail apps: {found['help']}")
        elif found.get('password') == 'bridge':
            ui.say('  use the password Proton Mail Bridge shows for this mailbox, not your Proton password')
        host = ui.ask('IMAP server', found.get('imap_host') or '').strip().lower()
        if not host or not re.fullmatch(r'[a-z0-9.:\[\]-]+', host):
            raise onboarding.SetupError('No IMAP server given', 'fill in Server settings with what your provider gives for mail apps')
        steer(email, imap_presets.OAUTH_HOSTS.get(host))
        if host in imap_mail.LOOPBACK and hosted(config):
            # a Machine we host can't reach a server on the owner's computer, like Proton Mail Bridge
            raise onboarding.SetupError('Proton Mail Bridge works only with The Machine on the same computer',
                                        'connect it from a Machine on the computer where Proton Mail Bridge runs')
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
        steer(email, imap_presets.OAUTH_HOSTS.get(account['smtp_host']))
    pin(account, ui)
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
        elif error.category == 'imap_tls_failed' and (names := wrong_name(account, 'imap')):
            # verification stays on: the owner gets the name the certificate is for, to type instead
            raise onboarding.SetupError(f'The mail server’s certificate is for {names[0]}, not {names[1]}',
                                        f'use {names[0]} as the IMAP server in Server settings') from None
        else:
            fix = 'check the server name, port and security in Server settings'
        raise onboarding.SetupError(what, fix) from None
    try:
        smtp_mail.check(config, None, account, password)
        account.pop('smtp_refused', None)
    except smtp_mail.SmtpError as error:
        account['smtp_refused'] = True  # reads; sending waits for a sign-in the SMTP server takes
        names = wrong_name(account, 'smtp') if error.category == 'smtp_tls_failed' else None
        if names:
            ui.say(f'  sending: the mail server’s certificate is for {names[0]}, not {names[1]}: use {names[0]} as the SMTP server in Server settings; reading only')
        else:
            ui.say(f"  sending: {REFUSED.get(error.category.replace('smtp_', 'imap_'), 'the mail server for sending didn’t answer as expected')}: reading only")
    if sent:
        account['sent_folder'] = sent
    else:
        account.pop('sent_folder', None)
        ui.say('  no Sent folder found: reading the inbox only')
    onboarding.write_private(path, password + '\n')
    ui.say('  signed in')
