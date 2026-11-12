"""The server settings for an email address, so most people type only their address and password (machine/sources/imap_setup.py).

In order, each a best effort that never blocks the setup: a small built-in table of known providers; the provider's own
autoconfig file (autoconfig.<domain>, then <domain>/.well-known); Mozilla's ISPDB (Thunderbird's provider database);
then the domain's mail servers (MX, through DNS over HTTPS) for hosting providers and for Google or Microsoft mail on a
company's own domain. Whatever it finds only fills in the form's server settings, which the owner can always change.

Gmail and Microsoft addresses, also on a company's own domain, are steered to their own connection (`oauth`): those
sign in with Google or Microsoft and need no password. A server offered only in plaintext is never used."""
import html
import json
import re
import urllib.parse
import urllib.request

TIMEOUT = 5  # seconds per lookup
MAX_ANSWER = 65536
DOH = 'https://cloudflare-dns.com/dns-query'

ZOHO_HELP = 'https://www.zoho.com/mail/help/adminconsole/two-factor-authentication.html#alink5'
# Known providers: the domains of their addresses -> their settings. `username`: 'email' (the whole address) or
# 'local' (the part before @). `help`: where to make the password a mail app needs, when the provider asks for one.
PROVIDERS = {
    'fastmail': {'domains': ('fastmail.com', 'fastmail.fm', 'fastmail.net', 'fastmail.org', 'fastmail.to', 'fastmail.us',
                             'sent.com', 'messagingengine.com'),
                 'imap': ('imap.fastmail.com', 993, 'ssl'), 'smtp': ('smtp.fastmail.com', 465, 'ssl'), 'username': 'email',
                 'name': 'Fastmail', 'help': 'https://www.fastmail.help/hc/en-us/articles/360058752854'},
    'icloud': {'domains': ('icloud.com', 'me.com', 'mac.com'),
               'imap': ('imap.mail.me.com', 993, 'ssl'), 'smtp': ('smtp.mail.me.com', 587, 'starttls'), 'username': 'local',
               'name': 'iCloud', 'help': 'https://support.apple.com/en-us/102654'},
    'yahoo': {'domains': ('yahoo.com', 'yahoo.co.uk', 'yahoo.fr', 'yahoo.de', 'yahoo.es', 'yahoo.it', 'yahoo.com.br',
                          'ymail.com', 'rocketmail.com'),
              'imap': ('imap.mail.yahoo.com', 993, 'ssl'), 'smtp': ('smtp.mail.yahoo.com', 465, 'ssl'), 'username': 'email',
              'name': 'Yahoo', 'help': 'https://help.yahoo.com/kb/SLN15241.html'},
    'aol': {'domains': ('aol.com',), 'imap': ('imap.aol.com', 993, 'ssl'), 'smtp': ('smtp.aol.com', 465, 'ssl'),
            'username': 'email', 'name': 'AOL'},
    'gmx': {'domains': ('gmx.de', 'gmx.net', 'gmx.at', 'gmx.ch'), 'imap': ('imap.gmx.net', 993, 'ssl'),
            'smtp': ('mail.gmx.net', 587, 'starttls'), 'username': 'email', 'name': 'GMX'},
    'gmx_com': {'domains': ('gmx.com', 'gmx.us', 'gmx.co.uk', 'gmx.fr', 'gmx.es'), 'imap': ('imap.gmx.com', 993, 'ssl'),
                'smtp': ('mail.gmx.com', 587, 'starttls'), 'username': 'email', 'name': 'GMX'},
    'webde': {'domains': ('web.de',), 'imap': ('imap.web.de', 993, 'ssl'), 'smtp': ('smtp.web.de', 587, 'starttls'),
              'username': 'email', 'name': 'WEB.DE'},
    'zoho': {'domains': ('zoho.com', 'zohomail.com'), 'imap': ('imap.zoho.com', 993, 'ssl'), 'smtp': ('smtp.zoho.com', 465, 'ssl'),
             'username': 'email', 'name': 'Zoho Mail', 'help': ZOHO_HELP},
    'zoho_eu': {'domains': ('zoho.eu', 'zohomail.eu'), 'imap': ('imap.zoho.eu', 993, 'ssl'), 'smtp': ('smtp.zoho.eu', 465, 'ssl'),
                'username': 'email', 'name': 'Zoho Mail', 'help': ZOHO_HELP},
    'zoho_in': {'domains': ('zoho.in', 'zohomail.in'), 'imap': ('imap.zoho.in', 993, 'ssl'), 'smtp': ('smtp.zoho.in', 465, 'ssl'),
                'username': 'email', 'name': 'Zoho Mail', 'help': ZOHO_HELP},
    'hawaiiantel': {'domains': ('hawaiiantel.net',), 'imap': ('imap.hawaiiantel.net', 993, 'ssl'),
                    'smtp': ('smtp.hawaiiantel.net', 465, 'ssl'), 'username': 'email', 'name': 'Hawaiian Telcom'},
    # Telenet (Belgium), as its own help pages give it: IMAP over SSL on 993, authenticated SMTP with TLS on 587, the full
    # address and the mail password
    'telenet': {'domains': ('telenet.be',), 'imap': ('imap.telenet.be', 993, 'ssl'), 'smtp': ('smtp.telenet.be', 587, 'starttls'),
                'username': 'email', 'name': 'Telenet', 'password': 'mail'},
    # Proton Mail through Proton Mail Bridge on this computer, with the password Bridge shows
    'proton': {'domains': ('proton.me', 'protonmail.com', 'protonmail.ch', 'pm.me'), 'imap': ('127.0.0.1', 1143, 'starttls'),
               'smtp': ('127.0.0.1', 1025, 'starttls'), 'username': 'email', 'name': 'Proton Mail', 'password': 'bridge'},
}


def _hosting(imap, smtp, name, port=465):
    return {'imap': (imap, 993, 'ssl'), 'smtp': (smtp, port, 'ssl'), 'username': 'email', 'name': name}


def _ionos(tld):
    return _hosting(f'imap.ionos.{tld}', f'smtp.ionos.{tld}', 'IONOS')


def _zoho_pro(region):  # mail on a company's own domain at Zoho: the servers Zoho gives paid organizations
    return {**_hosting(f'imappro.zoho.{region}', f'smtppro.zoho.{region}', 'Zoho Mail'), 'help': ZOHO_HELP}


# Hosting providers, known by the domain's mail servers (MX): mail on a domain of your own. Each one's servers for
# mail apps, IMAP over SSL/TLS on 993 and SMTP over SSL/TLS on 465, as checked against the servers themselves.
# 'same': the provider's mail apps sign in to the very server its MX names (one per customer group).
MX_PROVIDERS = {
    'ovh.net': _hosting('ssl0.ovh.net', 'ssl0.ovh.net', 'OVHcloud'),
    'one.com': _hosting('imap.one.com', 'send.one.com', 'one.com'),
    'mailprotect.be': _hosting('imap.mailprotect.be', 'smtp-auth.mailprotect.be', 'Combell'),
    'aruba.it': _hosting('imaps.aruba.it', 'smtps.aruba.it', 'Aruba'),
    'hostinger.com': _hosting('imap.hostinger.com', 'smtp.hostinger.com', 'Hostinger'),
    'privateemail.com': _hosting('mail.privateemail.com', 'mail.privateemail.com', 'Namecheap Private Email'),
    'emailsrvr.com': _hosting('secure.emailsrvr.com', 'secure.emailsrvr.com', 'Rackspace Email'),
    'infomaniak.ch': _hosting('mail.infomaniak.com', 'mail.infomaniak.com', 'Infomaniak'),
    'secureserver.net': _hosting('imap.secureserver.net', 'smtpout.secureserver.net', 'GoDaddy'),
    'loopia.se': _hosting('mailcluster.loopia.se', 'mailcluster.loopia.se', 'Loopia'),
    'rzone.de': _hosting('imap.strato.de', 'smtp.strato.de', 'STRATO'),
    'titan.email': _hosting('imap.titan.email', 'smtp.titan.email', 'Titan'),
    'your-server.de': _hosting('mail.your-server.de', 'mail.your-server.de', 'Hetzner'),
    'stackmail.com': _hosting('imap.stackmail.com', 'smtp.stackmail.com', '20i'),
    'mxrouting.net': {**_hosting('', '', 'MXroute'), 'same': True},
    'ionos.com': _ionos('com'), 'ionos.de': _ionos('de'), 'ionos.co.uk': _ionos('co.uk'), 'ionos.es': _ionos('es'),
    'ionos.fr': _ionos('fr'), 'ionos.it': _ionos('it'), 'ionos.mx': _ionos('mx'), 'kundenserver.de': _ionos('de'),
    'perfora.net': _ionos('com'),
    'messagingengine.com': PROVIDERS['fastmail'],
    'zoho.com': _zoho_pro('com'), 'zoho.eu': _zoho_pro('eu'), 'zoho.in': _zoho_pro('in'), 'zoho.com.au': _zoho_pro('com.au'),
}
# Mail that signs in with Google or Microsoft: its own connection, no password
OAUTH_DOMAINS = {'gmail.com': 'gmail', 'googlemail.com': 'gmail'}
OAUTH_MX = {'google.com': 'gmail', 'googlemail.com': 'gmail', 'outlook.com': 'outlook'}
# Their servers, also when typed in Server settings: Microsoft has turned off password sign-in there, and Google
# wants an app password where its own connection needs none
OAUTH_HOSTS = {'imap.gmail.com': 'gmail', 'smtp.gmail.com': 'gmail', 'imap.googlemail.com': 'gmail',
               'outlook.office365.com': 'outlook', 'smtp.office365.com': 'outlook', 'imap-mail.outlook.com': 'outlook',
               'smtp-mail.outlook.com': 'outlook', 'imap.outlook.com': 'outlook', 'smtp.outlook.com': 'outlook'}
MICROSOFT_CONSUMER = re.compile(r'(outlook|hotmail|live|msn|passport)\.[a-z]{2,3}(\.[a-z]{2})?')


def known_hosts(kind):
    """The mail servers ('imap' or 'smtp') of every provider above, for naming the right one when a certificate is
    made out to another name (imap_setup.name_to_use). Servers on this computer left out."""
    hosts = [entry[kind][0] for entry in (*PROVIDERS.values(), *MX_PROVIDERS.values()) if entry.get(kind) and entry[kind][0]]
    return list(dict.fromkeys(h for h in hosts if h != '127.0.0.1'))


def domain_of(email):
    return str(email or '').strip().lower().rpartition('@')[2]


def _shape(found, email, source):
    """A provider's entry as the account keys it fills in."""
    username = email if found.get('username', 'email') == 'email' else email.partition('@')[0]
    out = {'imap_host': found['imap'][0], 'imap_port': found['imap'][1], 'imap_security': found['imap'][2], 'username': username,
           'from': source}
    if found.get('smtp'):
        out.update(smtp_host=found['smtp'][0], smtp_port=found['smtp'][1], smtp_security=found['smtp'][2])
    for key in ('name', 'help', 'password'):
        if found.get(key):
            out[key] = found[key]
    return out


def builtin(email):
    domain = domain_of(email)
    for entry in PROVIDERS.values():
        if domain in entry['domains']:
            return _shape(entry, email, 'builtin')
    return None


def oauth_of(email):
    """'gmail' or 'outlook' when the address is plainly Google's or Microsoft's own mail, else None."""
    domain = domain_of(email)
    if domain in OAUTH_DOMAINS:
        return OAUTH_DOMAINS[domain]
    return 'outlook' if MICROSOFT_CONSUMER.fullmatch(domain) else None


def _fetch(url):
    """An https answer's text, small; None when it isn't there."""
    if not url.startswith('https://'):
        return None
    # DNS over HTTPS answers in JSON only when asked for it in Accept (a ct= parameter alone is refused with a 400)
    accept = 'application/dns-json' if url.startswith(DOH) else '*/*'
    request = urllib.request.Request(url, headers={'User-Agent': 'TheMachine-mail-setup', 'Accept': accept})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as reply:
            return reply.read(MAX_ANSWER + 1)[:MAX_ANSWER].decode('utf-8', 'replace')
    except (OSError, ValueError):
        return None


def parse_autoconfig(text, email):
    """Thunderbird's autoconfig XML: the first IMAP server and first SMTP server with TLS (SSL or STARTTLS); a plain
    one is skipped. None when it has no usable IMAP server. Read with a few patterns, never an XML parser: the answer
    comes from the network, and a document with a DOCTYPE (entities) is refused outright."""
    text = str(text or '')
    if re.search(r'<!(DOCTYPE|ENTITY)', text, re.I):
        return None
    local = email.partition('@')[0]

    def field(block, name):
        found = re.search(rf'<{name}\b[^>]*>([^<]*)</{name}\s*>', block)
        return html.unescape(found[1]).strip() if found else ''

    def pick(tag, kind):
        for server in re.finditer(rf'<{tag}\b([^>]*)>(.*?)</{tag}\s*>', text, re.S):
            if (re.search(r'\btype\s*=\s*["\']([^"\']*)["\']', server[1]) or [None, ''])[1] != kind:
                continue
            block = server[2]
            security = {'SSL': 'ssl', 'STARTTLS': 'starttls'}.get(field(block, 'socketType').upper())
            host = field(block, 'hostname').lower()
            try:
                port = int(field(block, 'port'))
            except ValueError:
                continue
            if not security or not re.fullmatch(r'[a-z0-9.-]+', host) or not 0 < port < 65536:
                continue
            username = field(block, 'username') or '%EMAILADDRESS%'
            return host, port, security, username.replace('%EMAILADDRESS%', email).replace('%EMAILLOCALPART%', local)
        return None
    imap, smtp = pick('incomingServer', 'imap'), pick('outgoingServer', 'smtp')
    if not imap:
        return None
    found = {'imap': imap[:3], 'smtp': smtp[:3] if smtp else None, 'username': 'email'}
    out = _shape(found, email, 'autoconfig')
    out['username'] = imap[3] if '%' not in imap[3] else email
    name = field(text, 'displayShortName')
    if name and len(name) < 60 and '%' not in name:  # some files leave a placeholder (%EMAILADDRESS%) there
        out['name'] = name
    return out


def mx_hosts(domain, fetch=_fetch):
    """The domain's mail servers, from DNS over HTTPS (only the domain is asked, never the address)."""
    text = fetch(DOH + '?' + urllib.parse.urlencode({'name': domain, 'type': 'MX'}))
    try:
        answers = json.loads(text or '{}').get('Answer') or []
    except ValueError:
        return []
    hosts = []
    for answer in answers:
        parts = str(answer.get('data') or '').split()
        if answer.get('type') == 15 and len(parts) == 2:
            hosts.append((int(parts[0]) if parts[0].isdigit() else 99, parts[1].rstrip('.').lower()))
    return [h for _, h in sorted(hosts)]


def _mx_match(host, table):
    return next((v for suffix, v in table.items() if host == suffix or host.endswith('.' + suffix)), None)


def lookup(email, fetch=_fetch, network=True):
    """The settings for this address: {imap_host, imap_port, imap_security, username, smtp_*, name, help, password, from}
    or {'oauth': 'gmail'|'outlook'} for mail that signs in with Google or Microsoft, or {} when nothing is known.
    Every lookup is a best effort: a slow or missing answer is skipped."""
    email = str(email or '').strip().lower()
    domain = domain_of(email)
    if not domain or not re.fullmatch(r'[a-z0-9.-]+\.[a-z]{2,}', domain):
        return {}
    oauth = oauth_of(email)
    if oauth:
        return {'oauth': oauth}
    known = builtin(email)
    if known or not network:
        return known or {}
    for url in (f'https://autoconfig.{domain}/mail/config-v1.1.xml?' + urllib.parse.urlencode({'emailaddress': email}),
                f'https://{domain}/.well-known/autoconfig/mail/config-v1.1.xml',
                f'https://autoconfig.thunderbird.net/v1.1/{domain}'):
        found = parse_autoconfig(fetch(url), email)
        if found:
            if found['imap_host'] in OAUTH_HOSTS:
                return {'oauth': OAUTH_HOSTS[found['imap_host']]}
            return found
    for host in mx_hosts(domain, fetch)[:3]:
        if _mx_match(host, OAUTH_MX):
            return {'oauth': _mx_match(host, OAUTH_MX)}
        entry = _mx_match(host, MX_PROVIDERS)
        if entry and entry.get('same'):
            entry = {**entry, 'imap': (host, *entry['imap'][1:]), 'smtp': (host, *entry['smtp'][1:])}
        if entry:
            return _shape(entry, email, 'mx')
        base = '.'.join(host.split('.')[-2:])
        found = parse_autoconfig(fetch(f'https://autoconfig.thunderbird.net/v1.1/{base}'), email) if base != domain else None
        if found:
            return {**found, 'from': 'mx'}
    return {}
