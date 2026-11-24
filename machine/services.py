"""Every service a connection can read (an account's `service` in config.json: 'gmail', 'slack', 'web_page'), with what
the code knows about each. A leaf: data only, it imports nothing, so any module and the dashboard (as JSON in the page,
dashboard_parts.kinds_json) can read it. A new service gets its row here; code asks this module instead of keeping a
map of services of its own. machine/kinds.py is the same for the kinds of event a service stores.

A service's row:
- name: what the owner calls it on a line that names the service (machine/names.SERVICES, service_name): 'Gmail'.
  None for a key that is no service of its own (google_docs: a Docs connection's Google provider, for its group).
- label: what + Add and setup call a built-in source (onboarding.LABELS): 'Other email'. None for a source with a
  connector file (connectors/*.py), whose label is its SETUP['label'].
- short: what the dashboard's status and error lines call it ("Signed out of Gmail", "Slack had a problem on its
  side", the Connect button of a to-do that needs it; Gmail is 'Gmail' and 'imap' is 'Other email' on every line): the page's SERVICE_NAMES (dashboard/todos-cards.js).
- sharing: what Fleet, Sharing calls a connection of it in "Your connections" (dashboard/fleet-sharing.js), None
  where it says `short`.
- unit: what a connection card counts ("1,204 events"), None for messages (dashboard/connections-cards.js).
- group: its + Add group (machine/sources/groups.py GROUPS): mail, calendar, chat, ... None where its connector's
  SETUP['group'] says it, else Other (groups.group_of). The calendar group is every calendar the page knows
  (CALENDAR_SERVICES).
- last: a catch-all source ("Other email": any other provider), shown after the A to Z rows of its group.
- signin: the sign-in through the control plane that connects it from the dashboard (fleet.SIGNIN_OF): Google for
  Gmail and Google Calendar together. None for one connected another way.
- transports: the internal tools an account without a `service` of its own names in its `transport` instead
  (names.TRANSPORT_SERVICES): an account with transport 'gog' is Gmail.
- read_now: its newest messages can be read at any minute by a read of the account, without the shared browser: what
  Send later waits for before a message goes (machine/app/send_later.py). Not Slack, where it reads the conversation.
- video: for a video call service, the key a meeting booked with it keeps (meet.VIDEO, meet_sessions.video), named
  by its `short` name; video_links: the parts of an address that are a link to such a call (meet.VIDEO_LINKS).

Where names disagree, each is kept as it is today and said here, never picked silently:
- name and label: 'caldav' and 'ics' are both 'Calendar' on a line, 'Other calendar' and 'Calendar link (ICS)' in + Add; 'exchange' is 'Exchange' and 'Exchange Server';
  'salesflare' is 'Salesflare' and 'Salesflare CRM'; 'android' is 'Android' and 'Android notifications'; 'telegram'
  and 'signal' are 'Telegram' and 'Signal' on a line, 'Telegram chats' and 'Signal chats' in + Add.
- short and name: 'calendar' is 'Calendar'
  and 'Google Calendar'; 'teams' is 'Teams' and 'Microsoft Teams'; 'rss' is 'Feed' and 'RSS'; 'docs' is 'Microsoft
  OneDrive' and 'Docs'; 'telegram', 'signal', 'android' and 'salesflare' say their + Add label.
- video and the service key: a booking keeps Google Meet as 'meet', not 'google_meet' (stored in meet_sessions, so it
  stays); a booking names Teams 'Teams', its `short` name.
- sharing and label: 'telegram' is 'Telegram' and 'salesflare' 'Salesflare' in Sharing, the rest that have one say
  their + Add label there.
"""

LAYER = 0  # every service a connection reads, with what the code knows of each (a leaf)

MAIL, CALENDAR, CHAT, MEETINGS, DOCS, CUSTOMERS, WORK, OTHER = 'mail', 'calendar', 'chat', 'meetings', 'docs', 'customers', 'work', 'other'
GROUPS = (MAIL, CALENDAR, CHAT, MEETINGS, DOCS, CUSTOMERS, WORK, OTHER)  # + Add's groups, in the order its list shows them

_NO = {'label': None, 'short': None, 'sharing': None, 'unit': None, 'group': None, 'last': False, 'read_now': False, 'signin': None, 'transports': (),
       'video': None, 'video_links': ()}

SERVICES = {
    # mail and calendars
    'gmail': {**_NO, 'name': 'Gmail', 'read_now': True, 'label': 'Gmail', 'short': 'Gmail', 'sharing': 'Gmail', 'group': MAIL, 'signin': 'google',
              'transports': ('gog', 'gogcli', 'himalaya')},
    'calendar': {**_NO, 'name': 'Google Calendar', 'label': 'Google Calendar', 'short': 'Calendar', 'sharing': 'Google Calendar',
                 'unit': 'events', 'group': CALENDAR, 'signin': 'google'},
    'outlook': {**_NO, 'name': 'Outlook', 'read_now': True, 'label': 'Outlook', 'short': 'Outlook', 'sharing': 'Outlook', 'group': MAIL, 'signin': 'microsoft',
                'transports': ('msgraph', 'msgraph-cli')},
    'outlook_calendar': {**_NO, 'name': 'Outlook Calendar', 'label': 'Outlook Calendar', 'short': 'Outlook Calendar',
                         'sharing': 'Outlook Calendar', 'unit': 'events', 'group': CALENDAR, 'signin': 'microsoft'},
    'imap': {**_NO, 'name': 'Other email', 'read_now': True, 'label': 'Other email', 'short': 'Other email', 'group': MAIL, 'last': True},
    'icloud_calendar': {**_NO, 'name': 'iCloud Calendar', 'label': 'iCloud Calendar', 'short': 'iCloud Calendar', 'sharing': 'iCloud Calendar',
                        'unit': 'events', 'group': CALENDAR},
    'caldav': {**_NO, 'name': 'Calendar', 'label': 'Other calendar', 'short': 'Calendar', 'sharing': 'Other calendar', 'unit': 'events',
               'group': CALENDAR, 'last': True},
    'proton_calendar': {**_NO, 'name': 'Proton Calendar', 'label': 'Proton Calendar', 'short': 'Proton Calendar', 'sharing': 'Proton Calendar',
                        'unit': 'events', 'group': CALENDAR},
    'ics': {**_NO, 'name': 'Calendar', 'label': 'Calendar link (ICS)', 'short': 'Calendar', 'sharing': 'Calendar link (ICS)', 'unit': 'events',
            'group': CALENDAR, 'last': True},
    'exchange': {**_NO, 'name': 'Exchange', 'label': 'Exchange Server', 'short': 'Exchange', 'sharing': 'Exchange Server', 'unit': 'events',
                 'group': CALENDAR},
    # chat, customers, the owner's phone
    'slack': {**_NO, 'name': 'Slack', 'label': 'Slack', 'short': 'Slack', 'sharing': 'Slack', 'group': CHAT, 'signin': 'slack'},
    'salesflare': {**_NO, 'name': 'Salesflare', 'label': 'Salesflare CRM', 'short': 'Salesflare CRM', 'sharing': 'Salesflare', 'group': CUSTOMERS,
                   'transports': ('salesflare-rest',)},
    'salesforce': {**_NO, 'name': 'Salesforce', 'short': 'Salesforce', 'unit': 'updates', 'group': CUSTOMERS, 'signin': 'salesforce'},
    'android': {**_NO, 'name': 'Android', 'label': 'Android notifications', 'short': 'Android notifications', 'unit': 'notifications',
                'transports': ('openclaw-feed', 'existing_openclaw_feed')},
    'whatsapp': {**_NO, 'name': 'WhatsApp', 'read_now': True, 'label': 'WhatsApp', 'short': 'WhatsApp', 'sharing': 'WhatsApp', 'group': CHAT,
                 'transports': ('wacli', 'wacli-local', 'existing_wacli_local_store')},
    'telegram': {**_NO, 'name': 'Telegram', 'read_now': True, 'label': 'Telegram chats', 'short': 'Telegram chats', 'sharing': 'Telegram', 'group': CHAT,
                 'transports': ('telegram_mirror', 'telegram_mirror_store')},
    'signal': {**_NO, 'name': 'Signal', 'read_now': True, 'label': 'Signal chats', 'short': 'Signal chats', 'sharing': 'Signal chats', 'group': CHAT,
               'transports': ('signal_mirror', 'signal_mirror_store')},
    'linkedin': {**_NO, 'name': 'LinkedIn', 'short': 'LinkedIn', 'sharing': 'LinkedIn', 'group': CHAT, 'transports': ('linkedin-inbox',)},
    'x': {**_NO, 'name': 'X', 'short': 'X', 'sharing': 'X', 'group': CHAT, 'transports': ('x-inbox',)},
    'intercom': {**_NO, 'name': 'Intercom', 'read_now': True, 'short': 'Intercom', 'sharing': 'Intercom', 'unit': 'conversations', 'group': CUSTOMERS,
                 'signin': 'intercom'},
    # meetings, work, docs and the rest
    'zoom': {**_NO, 'name': 'Zoom', 'short': 'Zoom', 'group': MEETINGS, 'signin': 'zoom', 'video': 'zoom', 'video_links': ('zoom.us/',)},
    'stripe': {**_NO, 'name': 'Stripe', 'short': 'Stripe', 'unit': 'events', 'group': CUSTOMERS, 'signin': 'stripe'},
    'github': {**_NO, 'name': 'GitHub', 'short': 'GitHub', 'unit': 'notifications', 'group': WORK, 'transports': ('gh',)},
    'trello': {**_NO, 'name': 'Trello', 'short': 'Trello', 'unit': 'card changes', 'group': WORK, 'signin': 'trello'},
    'shortcut': {**_NO, 'name': 'Shortcut', 'short': 'Shortcut', 'group': WORK, 'signin': 'shortcut'},
    'linear': {**_NO, 'name': 'Linear', 'short': 'Linear', 'unit': 'items', 'group': WORK, 'signin': 'linear'},
    'docs': {**_NO, 'name': 'Docs', 'short': 'Microsoft OneDrive', 'unit': 'items', 'group': DOCS, 'signin': 'microsoft_docs'},
    'notion': {**_NO, 'name': 'Notion', 'short': 'Notion', 'unit': 'items', 'group': DOCS, 'signin': 'notion'},
    'google_meet': {**_NO, 'name': 'Google Meet', 'short': 'Google Meet', 'unit': 'meetings', 'group': MEETINGS, 'signin': 'google_meet',
                    'video': 'meet', 'video_links': ('meet.google.com/',)},
    # after Zoom and Google Meet: a tie between video links goes to the first row (meet.video_habit)
    'teams': {**_NO, 'name': 'Microsoft Teams', 'read_now': True, 'short': 'Teams', 'group': CHAT, 'signin': 'microsoft_teams',
              'video': 'teams', 'video_links': ('teams.microsoft.com/', 'teams.live.com/')},
    'granola': {**_NO, 'name': 'Granola', 'short': 'Granola', 'unit': 'meetings', 'group': MEETINGS},
    'rss': {**_NO, 'name': 'RSS', 'short': 'Feed', 'unit': 'items'},
    'web_page': {**_NO, 'name': 'Web page', 'short': 'Web page', 'unit': 'updates'},
    'gateway': {**_NO, 'name': 'Machine health', 'label': 'Machine health', 'short': 'Machine health', 'unit': 'alerts',
                'transports': ('journald',)},
    'google_docs': {**_NO, 'name': None, 'group': DOCS},
}
# What the page gets of each row (dashboard_parts.kinds_json): only what its scripts read
PAGE_FIELDS = ('short', 'sharing', 'unit', 'group')


def of(*, group=None, signin=None, flag=None):
    """The services whose row matches every field given, in this module's order: of(group=MAIL) is
    ('gmail', 'outlook', 'imap'). A tuple, so callers can use it where a hand-written one was."""
    want = {'group': group, 'signin': signin}
    return tuple(key for key, row in SERVICES.items()
                 if all(value is None or row[field] == value for field, value in want.items()) and (flag is None or row[flag]))


def field(name):
    """{service: its value} for every service with a value in this field: field('name') is names.SERVICES."""
    return {key: row[name] for key, row in SERVICES.items() if row[name]}


def transports():
    """{transport: service}: what an account's transport says its service is, when it has none of its own."""
    return {transport: key for key, row in SERVICES.items() for transport in row['transports']}


def page():
    """The rows as the page carries them: {service: {field: value}} with PAGE_FIELDS only."""
    return {key: {name: row[name] for name in PAGE_FIELDS} for key, row in SERVICES.items()}
