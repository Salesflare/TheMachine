"""Setting up the calendars beyond Google and Outlook, from + Add (onboarding.web_form shows the forms):
iCloud Calendar and Other calendar over CalDAV (caldav_calendar.py), Proton Calendar and Calendar link from a calendar's
share link (ics_feed.py), and Exchange Server over EWS (ews_calendar.py). All read only.

Each one is checked before anything is saved: the password by signing in and finding the calendars, a link by reading
it. The password or link goes to a credential file (onboarding.write_private), never the config, a log or an error.
onboarding imports this module, so this one imports onboarding where it is used."""
import re
from pathlib import Path

import caldav_calendar
from caldav_calendar import CalendarError
import ews_calendar
import ics_feed
from machine.sources.imap_setup import given

SERVICES = ('icloud_calendar', 'caldav', 'proton_calendar', 'ics', 'exchange')
CALDAV, ICS = ('icloud_calendar', 'caldav'), ('proton_calendar', 'ics')
TRANSPORTS = {'icloud_calendar': 'caldav', 'caldav': 'caldav', 'proton_calendar': 'ics', 'ics': 'ics', 'exchange': 'ews'}
ACCOUNTS = {s: {'id': 'work-' + s.replace('_', '-'), 'service': s, 'transport': TRANSPORTS[s], 'calendar_id': 'primary',
                'boundary': 'work:Acme', 'exclude': []} for s in SERVICES}
LABELS = {'icloud_calendar': 'iCloud Calendar', 'caldav': 'Other calendar', 'proton_calendar': 'Proton Calendar',
          'ics': 'Calendar link (ICS)', 'exchange': 'Exchange Server'}
WHAT = {'icloud_calendar': 'Your iCloud meetings, so you go in prepared. Read-only.',
        'caldav': 'Meetings from a CalDAV calendar: Fastmail, Nextcloud, Zoho. Read-only.',
        'proton_calendar': 'Your Proton Calendar, through its share link. Read-only.',
        'ics': 'Any calendar link: published, school or sports calendars. Read-only.',
        'exchange': 'Meetings from your company’s own Exchange Server. Read-only.'}
NOTES = {'icloud_calendar': 'Use an app-specific password, made at https://appleid.apple.com under Sign-In and Security. '
                            'The one your iCloud Mail uses here works too.',
         'caldav': 'Many providers need an app password. Server settings are filled in for most.',
         'proton_calendar': 'In Proton Calendar on the web: Settings, All settings, Calendars, pick the calendar, then Share '
                            'with anyone, Create link, Full view. Copy the link and paste it here.',
         'ics': 'Paste the calendar’s https or webcal link. Anyone with it can read the calendar, so it is kept like a password.',
         'exchange': 'For an Exchange Server your company runs. Microsoft 365 connects with Outlook Calendar instead.'}
LEARN = {'icloud_calendar': 'other-calendars', 'caldav': 'other-calendars', 'proton_calendar': 'calendar-link',
         'ics': 'calendar-link', 'exchange': 'exchange'}
SECRETS = {'icloud_calendar': 'App-specific password', 'caldav': 'Password', 'proton_calendar': 'Share link',
           'ics': 'Calendar link', 'exchange': 'Password'}
ASKS = {'icloud_calendar': [['email', 'Apple ID']], 'caldav': [['email', 'Email address']],
        'exchange': [['email', 'Email address']]}
FIELDS = {'icloud_calendar': [['calendar_name', 'Only this calendar']],
          'caldav': [['username', 'Username'], ['caldav_url', 'CalDAV server'], ['calendar_name', 'Only this calendar']],
          'exchange': [['username', 'Username (DOMAIN\\name)'], ['ews_url', 'Exchange server']]}
IDENTITY = {'username', 'caldav_url', 'caldav_home', 'calendar_name', 'ews_url', 'ews_auth'}  # never copied to another one
HINTS = (  # onboarding.hint: what to do about a sync error
    ('caldav_auth_failed', 'the calendar server refused the password: connect it again (many providers need an app password)'),
    ('caldav_tls_failed', 'no secure connection to the calendar server: check its address'),
    ('caldav_unreachable', 'could not reach the calendar server; it retries by itself'),
    ('caldav_no_calendar', 'no calendar with events on the server: check Only this calendar in Server settings'),
    ('caldav_password_missing', 'the calendar has no saved password: connect it again'),
    ('caldav', 'the calendar server did not answer as expected; it retries by itself'),
    ('ics_gone', 'the calendar link stopped working: make a new one and connect it again'),
    ('ics_link_missing', 'the calendar has no saved link: connect it again'),
    ('ics', 'the calendar link did not answer as expected; it retries by itself'),
    ('exchange_online', 'this is a Microsoft 365 mailbox: connect Outlook Calendar instead'),
    ('ews_auth_failed', 'Exchange refused the username or password: connect it again'),
    ('ews_tls_failed', 'no secure connection to the Exchange server: check its address'),
    ('ews_password_missing', 'the Exchange calendar has no saved password: connect it again'),
    ('ews', 'the Exchange server did not answer as expected; it retries by itself'),
)
REFUSED = {
    'auth_failed': 'The server refused the username or password',
    'tls_failed': 'Couldn’t make a secure connection to the server',
    'unreachable': 'Couldn’t reach the server',
    'not_found': 'Couldn’t find a calendar on this server',
    'no_calendar': 'Couldn’t find a calendar with that name',
    'not_configured': 'Couldn’t find the server for this address',
    'redirect_refused': 'The server sent the sign-in somewhere else',
    'plaintext_refused': 'The Machine only connects over https',
    'gone': 'That link doesn’t open a calendar',
    'not_a_calendar': 'That link doesn’t open a calendar',
    'rate_limited': 'The server asked to slow down',
    'exchange_online': 'This is a Microsoft 365 mailbox',
    'other': 'The server didn’t answer as expected',
    'link': 'That link didn’t answer as expected',
}
MISSING = {'Apple ID': 'No Apple ID given', 'Email address': 'No email address given',
           'App-specific password': 'No app-specific password given', 'Password': 'No password given',
           'Share link': 'No share link given', 'Calendar link': 'No calendar link given'}
EMAIL = re.compile(r'[^@\s]+@[^@\s]+\.[^@\s]+')


def refused(error, service):
    """The SetupError for a CalendarError at setup: what happened, and what to do, in one line each."""
    import onboarding  # noqa: PLC0415 - onboarding imports this module
    if error.category == 'exchange_online':
        return onboarding.SetupError(REFUSED['exchange_online'], 'connect Outlook Calendar instead: it needs no password')
    kind = re.sub(r'^(caldav|ics|ews|calendar)_?', '', error.category)
    what = REFUSED.get(kind) or REFUSED['link' if service in ICS else 'other']
    if kind == 'auth_failed':
        fix = ('use an app-specific password from https://appleid.apple.com' if service == 'icloud_calendar'
               else 'check the username (DOMAIN\\name) and password' if service == 'exchange'
               else 'check the password; many providers need an app password')
    elif service in ICS:
        fix = 'copy the link again and paste it whole'
    else:
        fix = 'check the server in Server settings'
    return onboarding.SetupError(what, fix)


def _option(ui, prompt):
    """A folded-away setting: as the form gave it, or asked in a terminal (Enter leaves it)."""
    value = given(ui, prompt)
    if value is None and not getattr(ui, 'answers', None):
        value = ui.ask(prompt + ' (Enter leaves it)', '')
    return str(value or '').strip()


def _secret(config, account, ui, prompt):
    """(path, value) of the account's password or link: typed, or the saved one kept."""
    import onboarding  # noqa: PLC0415 - onboarding imports this module
    account['credential'] = account['transport'] + '-' + account['id']
    path = Path(config.setdefault('credentials', {}).setdefault(account['credential'], str(onboarding.data_dir(config) / account['credential']))).expanduser()
    has = path.exists() and bool(path.read_text().strip())
    value = ui.secret(prompt + (' (Enter keeps the saved one)' if has else ''))
    if not value and has:
        value = path.read_text().strip()
    if not value:
        raise onboarding.SetupError(MISSING[prompt], 'fill it in on the form')
    return path, value


def step(config, account, ui):
    """Any of SERVICES: what it signs in with, checked against the server before anything is saved. Signing in again
    asks only for the password (or link)."""
    import onboarding  # noqa: PLC0415 - onboarding imports this module
    service = account['service']
    account['transport'] = TRANSPORTS[service]
    account.setdefault('calendar_id', 'primary')
    again = getattr(ui, 'reconnect', False) and bool(account.get('email') or account.get('credential'))
    if service not in ICS and not again:
        prompt = ASKS[service][0][1]
        email = ui.ask(prompt, account.get('email') or '').strip().lower()
        if not EMAIL.fullmatch(email):
            raise onboarding.SetupError(MISSING[prompt], 'fill it in on the form')
        account['email'] = email
        for key, prompt in FIELDS[service]:
            value = _option(ui, prompt)
            if value:
                account[key] = value[:200]
            else:
                account.pop(key, None)
        if service == 'exchange' and not account.get('ews_url') and ews_calendar.microsoft_365(email):
            raise refused(CalendarError('exchange_online'), service)
    elif service in ICS:
        account.setdefault('email', '')
    path, secret = _secret(config, account, ui, SECRETS[service])
    try:
        if service in CALDAV:
            if account.get('caldav_url'):
                account['caldav_url'] = caldav_calendar.https_url(account['caldav_url'])
            account['caldav_home'], names = caldav_calendar.check(account, secret)
            ui.say('  ' + (names[0] or 'calendar') + ' found' if len(names) == 1 else f'  {len(names)} calendars found')
        elif service in ICS:
            secret = caldav_calendar.https_url(secret)
            ics_feed.check(secret)
            ui.say('  calendar found')
        else:
            if account.get('ews_url'):
                account['ews_url'] = ews_calendar.server_url(account['ews_url'])
            ews_calendar.check(account, secret)
            ui.say('  calendar found')
    except CalendarError as error:
        raise refused(error, service) from None
    onboarding.write_private(path, secret + '\n')
    ui.say('  signed in' if service not in ICS else '  saved the link')
