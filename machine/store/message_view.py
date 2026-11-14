"""How one collected message reads in the message viewer (dashboard/events-email.js), whatever source it came from.

Every event kind reads as one of four views:

- email: a mail (Gmail, Outlook, a CRM's copy of one). The subject is the title, the sender by name with the address
  quiet, To and Cc as their own lines, the text in paragraphs.
- chat: a conversation (Slack, Teams, WhatsApp, Telegram, Intercom, LinkedIn, X messages). Turns by who said them.
- notification: a phone notification or an alert. The app, the time, its title and text once each.
- card: an item with a state (an issue, a task, a deal, a payment, a doc comment, meeting notes). Its title, where it
  is ("owner/repo #12"), a state, who made it, why it reached the owner, the text rendered.

A connector declares the view of each of its kinds in VIEWS (and the app its links open in, APP); a built-in kind is
in BUILT_IN. tests/test_message_view.py fails any connector kind without one, and checks every view against the rules
below on made-up data. The rules (docs/adding-a-source.md, "How a message reads"):

1. No raw ids, Unix timestamps or internal type names on screen; never an app's package id (android_text_shown).
2. Nothing said twice: the title, the header, the details and the body each say something the others don't.
3. Markup renders: markdown, Slack's mrkdwn and HTML (sanitized). No literal ** or <url|label> brackets.
4. People by name where a name is known, and the real author, not the bot that sent the notification. A bare address
   shows by the Graph's name for it wherever a sender shows (address_names); the address only when no name is known.
   The source's own name for an address comes first (sender_name), and a relay or bot address never shows outside email.
5. A short title, whole, never cut mid-word by the source.
6. Long bodies fold behind Show more (the dashboard does that).
7. "Open in …" sits left, under the content, for every kind that has a link (list rows too: list_row).
8. A meeting transcript reads as speaker turns with times of day, never its raw "[0:00:00]" stamps (transcript_turns).
"""
import datetime as dt
import email.utils
import json
import re
import sqlite3

import graph
from machine.cards import group_sender
from machine.sources.android import android_app_shown, android_text_shown
from machine.sources.gmail import phone_link
from machine.sources.slack import slack_plain
from machine.store import graph_identifiers
from mail_senders import relay

VIEWS =('email', 'chat', 'notification', 'card')

BUILT_IN = {'gmail.message': 'email', 'ms_graph.message': 'email', 'outlook.message': 'email', 'imap.message': 'email',
            'salesflare.email': 'email', 'fleet.email': 'email',
            'slack.message': 'chat', 'whatsapp.message': 'chat', 'telegram.message': 'chat', 'signal.message': 'chat', 'fleet.message': 'chat',
            'fleet.intercom': 'chat',
            'android.notification': 'notification', 'gateway.alert': 'notification', 'machine.system_log': 'notification',
            'calendar.event': 'card', 'outlook.event': 'card', 'ms_graph.event': 'card', 'salesflare.meeting': 'card',
            'meeting.notes': 'card', 'meeting.transcript': 'card', 'machine.fault': 'card', 'machine.parked_fix': 'card',
            'machine.moved': 'card', 'fleet.request': 'card'}

# The app a built-in kind's link opens in ("Open in Salesflare"); a connector names its own in APP
BUILT_IN_APP = {'gmail': 'Gmail', 'salesflare': 'Salesflare', 'slack': 'Slack', 'whatsapp': 'WhatsApp', 'telegram': 'Telegram',
                'calendar': 'Calendar', 'outlook': 'Outlook', 'ms_graph': 'Outlook'}

# Body formats the dashboard renders (events-email.js msgMarkdown): markdown, or plain text
MARKDOWN_KINDS = {'github.notification', 'github.ci', 'shortcut.move', 'trello.action', 'slack.message', 'whatsapp.message',
                  'telegram.message', 'teams.message', 'fleet.message', 'docs.comment', 'docs.mention', 'docs.suggestion',
                  'zoom.summary', 'google_meet.notes', 'teams.notes', 'meeting.notes'}


def _connector(kind):
    from machine.sources.connectors import load_connector  # here: the store loads before the connector registry
    service = str(kind).split('.')[0] if '.' in str(kind) else ''
    try:
        return load_connector(service) if service else None
    except Exception:  # a broken plugin never stops a message from reading
        return None


def view_of(kind):
    """The view an event kind reads in: BUILT_IN, else its connector's VIEWS, else a card."""
    if kind in BUILT_IN:
        return BUILT_IN[kind]
    plugin = _connector(kind)
    return (getattr(plugin, 'VIEWS', None) or {}).get(kind, 'card')


def app_of(kind, url=''):
    """The app a message's link opens in, by name ("GitHub"), or '' when there is none to name (then "Open original")."""
    service = str(kind).split('.')[0]
    if service == 'gmail' and re.match(r'https://outlook\.', str(url or '')):
        return 'Outlook'
    if service in BUILT_IN_APP:
        return BUILT_IN_APP[service]
    app = getattr(_connector(kind), 'APP', '') or ''
    if isinstance(app, dict):  # by the link's host: {'docs.google.com': 'Google Docs', 'sharepoint.com': 'OneDrive'}
        host = (re.match(r'https://([^/:]+)', str(url or '')) or [None, ''])[1].lower()
        return next((name for end, name in app.items() if host == end or host.endswith('.' + end)), '')
    return str(app)


def same(a, b):
    """Two texts that say the same thing (case, spaces and punctuation aside)."""
    norm = lambda s: re.sub(r'[\W_]+', ' ', str(s or '').casefold()).strip()
    return bool(norm(a)) and norm(a) == norm(b)


# A chat's photo, video or file without a caption is stored as the words "Sent image" (WhatsApp), "Sent a photo"
# (Telegram, Signal): the viewer shows what it is as a media chip instead of those words (media). The body keeps
# them for everything else that reads it (the to-do's chat, the model).
MEDIA = {'image': 'photo', 'photo': 'photo', 'view-once media': 'photo', 'video': 'video', 'gif': 'video', 'video note': 'video',
         'animation': 'video', 'audio': 'audio', 'voice': 'voice', 'ptt': 'voice', 'voice note': 'voice', 'sticker': 'sticker'}
MEDIA_KINDS = {'whatsapp.message', 'telegram.message', 'signal.message'}


def media_shown(kind, m, body):
    """{'media': what a chat message sent ('photo', 'video', 'audio', 'voice', 'sticker' or 'file'), 'media_only':
    True when its text is only the source's "Sent …" placeholder for it}, or {} when it sent none. A caption is
    text of its own and reads under the chip."""
    sent = str(m.get('media_type') or '').strip().lower().replace('_', ' ')
    if kind not in MEDIA_KINDS or not sent:
        return {}
    only = bool(re.fullmatch(r'Sent (?:an? )?' + re.escape(sent), str(body or '').strip(), re.I))
    return {'media': MEDIA.get(sent, 'file'), **({'media_only': True} if only else {})}


def drop_repeats(body, *said):
    """The body without leading lines that repeat something already shown (the title, the sender)."""
    lines = str(body or '').split('\n')
    while lines and (not lines[0].strip() or any(same(lines[0], s) for s in said if s)):
        lines.pop(0)
    return '\n'.join(lines)


# A body that starts with mail headers ("From: Sam Lee <sam@x.example>", "To: …"), as a CRM's copy of an email does: they
# go to the header and leave the text. Only a block of them at the very top with From or To among them, ended by a blank line.
HEADER = re.compile(r'^(From|To|Cc|Bcc|Reply-To|Date|Sent|Subject):[ \t]*(.*)$', re.I)


def header_lines(body):
    """({'from': [...], 'to': [...], ...}, the rest of the body) or ({}, body) when it doesn't start with header lines."""
    lines = str(body or '').replace('\r\n', '\n').split('\n')
    found, n = {}, 0
    for line in lines:
        m = HEADER.match(line)
        if not m:
            break
        found.setdefault(m[1].lower(), []).append(m[2].strip())
        n += 1
    if not n or not {'from', 'to'} & set(found) or (n < len(lines) and lines[n].strip()):
        return {}, body
    return found, '\n'.join(lines[n:]).strip('\n')


def _address(value):
    m = re.search(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+', str(value or ''))
    return m[0].lower() if m else ''


# A name-less address: "ann@client.com" or "<ann@client.com>", nothing else
BARE = re.compile(r'\s*<?([\w.+-]+@[\w-]+(?:\.[\w-]+)+)>?\s*')


def bare_addresses(*values):
    """The addresses in these From/To/Cc fields (or source lines' who) that carry no name, lowercased."""
    return {m[1].lower() for v in values for part in str(v or '').split(',') if (m := BARE.fullmatch(part))}


def address_names(db, addresses):
    """The Graph's name for each of these addresses (lowercased), for the people one is known for: never an address,
    nor a source's own name ("Slack", "Stripe": graph.SOURCE_NAMES), as the name. Empty without a Graph. Used wherever
    a sender shows: the viewer, a to-do's source line, the rows of "Checked N messages"."""
    addresses = sorted({str(a).lower() for a in addresses if a})
    if not addresses:
        return {}
    wanted = sorted({'email:' + a for a in addresses})
    marks = ','.join('?' * len(wanted))
    try:
        rows = [*db.execute(f"SELECT * FROM graph_nodes WHERE kind='person' AND id IN ({marks})", wanted),
                *graph_identifiers.rows(db, 'n.*', wanted, f"SELECT n.* FROM graph_nodes n, json_each(n.info,'$.identifiers') j "
                                        f"WHERE n.kind='person' AND j.value IN ({marks})", wanted)]
    except sqlite3.OperationalError:
        return {}  # no graph yet
    names = {}
    for row in rows:
        name = str(row['name'] or '').strip()
        if not name or '@' in name or name in graph.SOURCE_NAMES:
            continue
        try:
            ids = {row['id'], *(json.loads(row['info'] or '{}').get('identifiers') or ())}
        except (ValueError, AttributeError):
            ids = {row['id']}
        for i in ids & set(wanted):
            names.setdefault(i[6:], name)
    return names


# Where a source puts a sender's name when its `from` is an address (or empty), in the order they are read
NAME_KEYS = ('sender_display', 'from_name', 'contact_name', 'sender_name', 'user_name', 'customer_name')


def sender_name(kind, m):
    """Who sent a message, by name (rule 4), for every source: the name in `from` ("Sam Lee <sam@x.example>"), else
    the name the source gives beside it (NAME_KEYS: Intercom's from_name, a chat's sender_display), the address only
    when there is no name. A relay or bot address (Intercom's operator+…@intercom.io, a noreply) stands in for someone
    and never shows outside email: the conversation's customer by name when the source names one, else the bot or
    teammate by the name the source gives ("Fin"), else nothing."""
    raw = ' '.join(str(m.get('from') or '').split())
    names = [n for n in (' '.join(str(m.get(k) or '').split()) for k in NAME_KEYS) if n and '@' not in n]
    if '@' not in raw and '<' not in raw:
        return raw or (names[0] if names else '')  # a name as is, or none
    name, address = email.utils.parseaddr(raw)
    name = name.strip().strip('"')
    name = '' if '@' in name else name
    if relay(address) and view_of(kind) != 'email':
        customer = ' '.join(str(m.get('contact_name') or '').split())
        contact = str(m.get('contact_email') or '').strip()
        return ((customer if '@' not in customer else '') or (contact if '@' in contact and not relay(contact) else '')
                or name or (names[0] if names else ''))
    return name or (names[0] if names else '') or address


def named(value, names):
    """A From/To/Cc field with each name-less address the graph knows a name for written "Name <address>" (`names`:
    address -> name, from Store.address_names), so the viewer and source lines say the name, the address only when
    no name is known."""
    def one(part):
        m = BARE.fullmatch(part)
        name = m and names.get(m[1].lower())
        return (' ' if part[:1] == ' ' else '') + f'{name} <{m[1]}>' if name else part
    return ','.join(one(part) for part in str(value or '').split(',')) if value else value


def name_only(value, names):
    """A sender outside email (a chat's, a payment's) that is only an address, by the name the graph knows for it
    (`names`, from address_names); the address when none is known."""
    m = BARE.fullmatch(str(value or ''))
    return names.get(m[1].lower(), value) if m else value


def shape_email(o, m, title):
    found, body = header_lines(o['body'])
    if found:
        o['body'] = body
        froms = found.get('from') or []
        if froms and (not o.get('from') or '<' not in o['from'] or _address(froms[0]) == _address(o['from'])):
            o['from'] = froms[0][:300]
        for key, head in (('to', 'to'), ('cc', 'cc'), ('bcc', 'bcc'), ('reply_to', 'reply-to')):
            if found.get(head) and not o.get(key):
                o[key] = ', '.join(found[head])[:500]
    # A Google Group's "'Sam Lee' via Sales" <sales@…> as people say it: Sam Lee via Sales <sales@…>
    name, cut, rest = str(o.get('from') or '').partition('<')
    shown = group_sender(name.strip().strip('"'))
    if shown != name.strip().strip('"'):
        o['from'] = shown + (' <' + rest if cut else '')
    o['body'] = drop_repeats(o['body'], title)
    details_only(o)


def _domain(address):
    """The domain a mail service sends from, as Gmail's "via" says it: mail1.mcsv.example is mcsv.example."""
    host = _address(address).partition('@')[2].split('.')
    return '.'.join(host[-3:] if len(host) > 2 and len(host[-2]) <= 3 and len(host[-1]) == 2 else host[-2:])


def details_only(o):
    """An email's Details hold only what its header doesn't show (rule 2): a Reply-To only when it goes somewhere other
    than the sender, and the service it was sent through (sent_via, from the Sender header) only when that isn't the
    sender's own domain and the From doesn't already say it. Bcc stays (the header never shows it); To and Cc are the
    dashboard's to judge (mailHead), as their header line is drawn there."""
    sender = _address(o.get('from'))
    replies = {_address(part) for part in str(o.get('reply_to') or '').split(',')} - {''}
    if not replies or replies <= {sender}:
        o.pop('reply_to', None)
    via = _domain(o.pop('sender', '') or '')
    if via and sender and via != _domain(sender) and via not in str(o.get('from') or '').lower():
        o['sent_via'] = via


# Slack's mrkdwn (and WhatsApp's, which writes bold, italic and strike the same way) as markdown the dashboard renders:
# links without their brackets, channels and groups by name, never an id.
SLACK_SPECIAL = re.compile(r'<(!subteam\^[A-Z0-9]+|!here|!channel|!everyone|!date\^[^|>]*|#[CG][A-Z0-9]+|@[UW][A-Z0-9]+)(?:\|([^>]*))?>')
SLACK_LINK = re.compile(r'<((?:https?|mailto):[^|>\s]+)(?:\|([^>]*))?>')


def _slack_special(m):
    what, label = m[1], (m[2] or '').strip()
    if what in ('!here', '!channel', '!everyone'):
        return '@' + what[1:]
    if what.startswith('!subteam'):
        return label if label.startswith('@') else '@' + (label or 'team')
    if what.startswith('!date'):
        return label
    if what.startswith('#'):
        return '#' + (label or 'channel')
    return '@' + (label or 'someone on Slack')


def mrkdwn(text, slack=True):
    """Slack mrkdwn as markdown: *bold* **bold**, _italic_ *italic*, ~strike~ ~~strike~~, <url|label> [label](url)."""
    keep = []

    def hold(s):
        keep.append(s)
        return f'\u0000{len(keep) - 1}\u0001'
    text = re.sub(r'```[\s\S]*?```|`[^`\n]+`', lambda m: hold(m[0]), str(text or ''))  # code stays as written
    if slack:
        text = SLACK_SPECIAL.sub(_slack_special, text)
        text = SLACK_LINK.sub(lambda m: hold(f'[{m[2].strip()}]({m[1]})' if m[2] and m[2].strip() and m[2].strip() != m[1]
                                             else (m[1][7:] if m[1].startswith('mailto:') else m[1])), text)
    text = re.sub(r'https?://\S+', lambda m: hold(m[0]), text)  # an address's _ and * are not markup
    text = re.sub(r'(?<![\w*])\*(?=\S)([^*\n]+?)(?<=\S)\*(?![\w*])', r'**\1**', text)
    text = re.sub(r'(?<![\w_])_(?=\S)([^_\n]+?)(?<=\S)_(?![\w_])', r'*\1*', text)
    text = re.sub(r'(?<![\w~])~(?=\S)([^~\n]+?)(?<=\S)~(?![\w~])', r'~~\1~~', text)
    text = re.sub(r'^&gt;', '>', text, flags=re.M)
    return re.sub(r'\u0000(\d+)\u0001', lambda m: keep[int(m[1])], text)


# GitHub: "Issue in owner/repo (open); why you got it: author." on top, the issue's text, then "Latest comment by X:" and
# the comment (connectors/github.py). Newer events carry the same in metadata too.
GITHUB_HEAD = re.compile(r'^(\w[\w ]*?) in ([\w.-]+/[\w.-]+)(?: \((\w+)\))?; why you got it: ([\w ]+)\.\s*(?:\n|$)')
GITHUB_COMMENT = re.compile(r'(?:^|\n\n)Latest comment by ([^\n:]*):\n')
GITHUB_REASONS = {'author': 'author', 'mention': 'mention', 'team mention': 'team_mention', 'review requested': 'review_requested',
                  'assign': 'assign', 'comment': 'comment', 'state change': 'state_change', 'ci activity': 'ci_activity',
                  'subscribed': 'subscribed', 'manual': 'subscribed', 'security alert': 'security_alert', 'invitation': 'invitation'}
BOT = re.compile(r'\[bot\]$|-bot$|^(?:dependabot|renovate|github-actions)$', re.I)


def shape_github(o, m):
    o['title'] = re.sub(r'^\[[^\]\n]{1,100}\]\s*', '', o['title'])
    body = o['body']
    head = GITHUB_HEAD.match(body)
    repo = m.get('repo') or (head[2] if head else '')
    if head:
        body = body[head.end():].lstrip('\n')
    state = m.get('state') or (head[3] if head else '')
    reason = str(m.get('reason') or (head[4] if head else '')).replace('_', ' ')
    comment = GITHUB_COMMENT.search(body)
    by = comment[1].strip() if comment else ''
    said = body[comment.end():] if comment else ''
    issue = body[:comment.start()] if comment else body
    author = m.get('author') or ('' if comment else m.get('from') or '')
    number = m.get('number')
    o['card'] = {'ref': repo + (f' #{number}' if isinstance(number, int) else ''), 'state': str(state or '').lower(),
                 'type': str(m.get('type') or (head[1] if head else '')), 'reason': GITHUB_REASONS.get(reason, ''),
                 'author': author, 'bot': bool(author and BOT.search(author))}
    if comment:  # a comment: the comment is what's new; the issue's own text is context, folded
        o['card'].update(comment_by=by, comment_bot=bool(BOT.search(by)))
        o['body'] = said.strip()
        if issue.strip():
            o['context'] = issue.strip()
    else:
        o['body'] = issue.strip()
    o['from'] = author


def shape_notification(o, m, title):
    app = m.get('app_name') or ''
    o['app_name'] = app
    package = m.get('package_name') or ''
    raw_id = lambda text: bool(package) and not android_text_shown(text, package)  # a package id is no text (rule 1)
    if raw_id(title):
        o['title'] = title = ''
    lines = [line for line in str(o['body'] or '').split('\n') if line.strip() and not raw_id(line)]
    text = lines[0] if lines else ''
    sub = '\n'.join(lines[1:]) if len(lines) > 1 else ''
    if same(title, app):
        o['title'] = ''
    if same(text, o['title']) or same(text, app):
        text = ''
    if same(sub, o['title']) or same(sub, app) or same(sub, text):
        sub = ''
    o['body'], o['sub'] = text, sub
    o['from'] = ''


# Intercom: the opening message, then "<unix time> · <author> · <part type>: <text>" lines (connectors/intercom.py). Who
# wrote each part: the connector keeps author_roles (name -> customer, team or bot); older events are read by name.
INTERCOM_CHANNELS = {'facebook': 'Facebook', 'instagram': 'Instagram', 'whatsapp': 'WhatsApp', 'twitter': 'X', 'sms': 'SMS',
                     'email': 'Email', 'telegram': 'Telegram', 'line': 'LINE'}
INTERCOM_BOTS = re.compile(r'^(?:fin|operator|.*\bbot)$', re.I)


def intercom_role(name, m):
    roles = m.get('author_roles') if isinstance(m.get('author_roles'), dict) else {}
    if name in roles:
        return roles[name]
    customer = {str(m.get(k) or '').casefold() for k in ('contact_name', 'from_name', 'from', 'contact_email')} - {''}
    if str(name).casefold() in customer:
        return 'customer'
    return 'bot' if INTERCOM_BOTS.match(str(name).strip()) else 'team'


INTERCOM_PART = re.compile(r'^(\d{9,11}) · (.*?) · ([a-z_]+): ?(.*)$')


def intercom_turns(m, body, occurred_at):
    """The conversation as turns: [{'from', 'occurred_at', 'body', 'role', 'note'?}]. Parts with no text (assignments,
    attribute updates, state changes) are left out; a part's raw time and type never show."""
    who = m.get('contact_name') or m.get('from_name') or ''
    turns, opening = [], []
    for line in str(body or '').split('\n'):
        part = INTERCOM_PART.match(line)
        if part:
            turns.append({'from': part[2].strip(), 'at': int(part[1]), 'type': part[3], 'body': part[4]})
        elif turns:
            turns[-1]['body'] += '\n' + line
        else:
            opening.append(line)
    # The contact's own fields that some channels put on top of the opening message (their name, "Facebook"): not said
    noise = {str(m.get(k) or '').casefold() for k in ('contact_name', 'from_name', 'from', 'contact_email')} | {
        v.casefold() for v in INTERCOM_CHANNELS.values()}
    first = '\n'.join(line for line in opening if line.strip().casefold() not in noise - {''}).strip()
    start = m.get('created_at') if type(m.get('created_at')) is int else None
    out = [{'from': who or m.get('from') or '', 'role': 'customer', 'body': first,
            'occurred_at': dt.datetime.fromtimestamp(start, dt.timezone.utc).isoformat() if start else occurred_at}] if first else []
    for t in turns:
        if not t['body'].strip():
            continue
        out.append({'from': t['from'][:300], 'role': intercom_role(t['from'], m), 'body': t['body'].strip(),
                    'occurred_at': dt.datetime.fromtimestamp(t['at'], dt.timezone.utc).isoformat(),
                    **({'note': True} if t['type'] == 'note' else {})})
    return out


# A meeting transcript's turn, as Zoom, Teams, Meet and pasted ones write it: "[0:01:02] Dana: words", "00:01:02 Dana:
# words", "Dana (00:01): words", "Dana 0:01: words" or "Dana: words". A WebVTT cue's timing line ("00:00:01.000 -->
# 00:00:04.000") gives the next turn its time. The stamp is when in the meeting it was said (h:mm:ss or m:ss).
_STAMP = r'[\[(]?((?:\d{1,2}:)?\d{1,2}:\d{2})(?:[.,]\d{1,3})?[\])]?'
TURN_STAMP_FIRST = re.compile(r'^\s*(?:[-*]\s+)?' + _STAMP + r'\s*[-–|]?\s*([^\s:\[(][^:\n]{0,60}?)\s*:\s*(.*)$')
TURN_STAMP_AFTER = re.compile(r'^\s*(?:[-*]\s+)?([^\s:\[(][^:\n]{0,60}?)[\s,–-]+' + _STAMP + r'\s*:\s*(.*)$')
TURN_PLAIN = re.compile(r'^\s*(?:[-*]\s+)?([^\s:\[(\d][^:\n]{0,60}?):\s+(\S.*)$')
CUE = re.compile(r'^\s*' + _STAMP + r'\s+-->\s')


def transcript_kind(kind):
    """Whether an event kind is a meeting transcript (meeting.transcript, zoom.transcript, teams.transcript, a future
    connector's *.transcript)."""
    return str(kind or '').endswith('.transcript')


def _seconds(stamp):
    parts = [int(p) for p in str(stamp).split(':')]
    return parts[0] * 3600 + parts[1] * 60 + parts[2] if len(parts) == 3 else parts[0] * 60 + parts[1]


def transcript_turns(body, start=None):
    """A transcript as speaker turns, [{'from', 'body', 'occurred_at'}], without its raw stamps: a speaker's run is one
    turn, said at the meeting's start (`start`, ISO) plus its first stamp. A turn without a stamp keeps the time before
    it and is `untimed` (no time shown: never the same time over and over). [] when speaker lines aren't most of the
    text (then it reads as written)."""
    try:
        began = dt.datetime.fromisoformat(str(start)) if start else None
    except ValueError:
        began = None
    at = lambda secs: (began + dt.timedelta(seconds=secs)).isoformat() if began else (start or '')
    turns, cue, total, covered, last = [], None, 0, 0, 0
    for line in str(body or '').replace('\r\n', '\n').split('\n'):
        bare = line.strip()
        if not bare or bare == 'WEBVTT' or bare.isdigit():
            continue
        timing = CUE.match(line)
        if timing:
            cue = _seconds(timing[1])
            continue
        total += len(bare)
        hit = TURN_STAMP_FIRST.match(line)
        who, said, secs = (hit[2], hit[3], _seconds(hit[1])) if hit else (None, None, None)
        if not hit and (hit := TURN_STAMP_AFTER.match(line)):
            who, said, secs = hit[1], hit[3], _seconds(hit[2])
        if not hit and (hit := TURN_PLAIN.match(line)):
            who, said, secs = hit[1], hit[2], cue
        cue = None
        if not hit:
            if turns:  # a turn's words that went on to the next line
                turns[-1]['body'] += ' ' + bare
                covered += len(bare)
            continue
        covered += len(bare)
        who, said = ' '.join(who.split())[:120], said.strip()
        if turns and turns[-1]['from'] == who:
            turns[-1]['body'] = (turns[-1]['body'] + ' ' + said).strip()
        else:
            turns.append({'from': who, 'body': said, 'occurred_at': at(last if secs is None else secs)}
                         | ({'untimed': True} if secs is None else {}))
        last = last if secs is None else secs
    turns = [t for t in turns if t['body']]
    return turns if turns and covered >= 0.6 * total else []


def list_row(kind, title, body, m, occurred_at=''):
    """How one message reads as a row in a list of them (Messages, events-list.js), by the same rules as the viewer:
    {'title', 'who', 'text', 'url', 'phone_url'?, 'app'}. `who` is who it's from by name (never an address, a package or
    the title again), `text` its words without raw stamps, ids or markup, `url` where it opens outside (https only,
    else ''), and `app` the app that is ("Gmail"; '' is "Open original"). Every kind with a link gets it, the same way."""
    m = m if isinstance(m, dict) else {}
    view = view_of(kind)
    title, text = ' '.join(str(title or '').split()), str(body or '')
    who, turns = '', []
    if view == 'notification':
        package = str(m.get('package_name') or '')
        app = android_app_shown(package, m.get('app_name')) if package else str(m.get('app_name') or '')
        o = {'title': title, 'body': text}
        shape_notification(o, {**m, 'app_name': app}, title)
        title = o['title'] or app
        text = '\n'.join(s for s in (o['body'], o['sub']) if s and not same(s, title))
        who = app
    elif transcript_kind(kind) and (turns := transcript_turns(text[:6000], m.get('start_at') or occurred_at)):  # its start is enough
        text = '\n'.join(f"{t['from']}: {t['body']}" for t in turns)
    elif kind in ('intercom.conversation', 'fleet.intercom') and (said := intercom_turns(m, text, occurred_at)):
        # a support conversation by who said what, never its parts' raw times and types; the customer's own words
        # without their name again (the meta line says it)
        who = sender_name(kind, m)
        text = '\n'.join(t['body'] if t['from'] == who else f"{t['from']}: {t['body']}" for t in said)
    else:  # as the viewer shapes it (shape): mail headers out of the text, GitHub's head line and its comment's author
        o = shape(kind, {'title': title, 'body': text, 'from': str(m.get('from') or ''), 'occurred_at': occurred_at, 'url': None}, dict(m))
        title, text = ' '.join(str(o.get('title') or title).split()), o.get('body') or ''
        if o['format'] == 'markdown':  # a row is plain words: no ** or [label](url)
            text = plain_markdown(text)
        if kind != 'calendar.event':  # a meeting's row says when, not who
            card = o.get('card') or {}
            # a Google Group's "'Sam Lee' via Sales" is Sam Lee
            raw = str(o.get('from') or '')
            person = (raw.partition('<')[0] if '<' in raw else '').strip().strip('"').split(' via ')[0].strip().strip("'\"")
            # the owner's own: a chat row says "From You" (events-list.js); anything else of theirs needs no sender
            who = ('You' if kind in ('whatsapp.message', 'linkedin.message') else '') if m.get('from_me') else card.get('comment_by') or (person if view == 'email' and '@' not in person else '') \
                or sender_name(kind, {**m, 'from': o.get('from') or m.get('from')}) or str(m.get('channel_name') or m.get('chat_name') or '')
            who = re.sub(r'\[bot\]$', '', who, flags=re.I)  # "sweeper", as the viewer names a bot
    who = ' '.join(who.split())
    if who and (words_in(who) <= words_in(title)):  # the title says it already ("Jamie Morgan", "#general: Tomasz Nowak")
        who = ''
    url = m.get('source_url')
    url = url if isinstance(url, str) and re.match(r'https://[^\s/]+', url) else ''
    row = {'title': title, 'who': who, 'text': text.strip()[:2000], 'url': url, 'app': app_of(kind, url) if url else ''}
    if turns:  # a transcript's first turns, each by its speaker (the row shows three lines)
        row['turns'] = [{'from': t['from'], 'body': t['body'][:300]} for t in turns[:6]]
    if url and kind == 'gmail.message':
        phone = phone_link(url, m.get('thread_id'))
        if phone:
            row['phone_url'] = phone
    return row


def plain_markdown(text):
    """Markdown as the plain words a list row shows: [label](url) as label, no ** _ ` or # marks, code as its text."""
    text = re.sub(r'```[^\n]*\n?([\s\S]*?)```', r'\1', str(text or ''))
    text = re.sub(r'!?\[([^\]\n]*)\]\((?:[^()\s]|\([^()\s]*\))+\)', r'\1', text)
    text = re.sub(r'(?m)^\s{0,3}#{1,6}\s+', '', text)
    text = re.sub(r'(\*\*|__|~~)(?=\S)(.+?)(?<=\S)\1', r'\2', text)
    text = re.sub(r'(?<![\w*])\*(?=\S)([^*\n]+?)(?<=\S)\*(?![\w*])', r'\1', text)
    return re.sub(r'`([^`\n]+)`', r'\1', text)


def list_rows(db, events):
    """list_row for each event (dicts with kind, title, body, metadata, occurred_at), a sender known only by address
    by the Graph's name for it (rule 4); the address only when no name is known."""
    rows = [list_row(e.get('kind'), e.get('title'), e.get('body'), e.get('metadata'), e.get('occurred_at')) for e in events]
    names = address_names(db, bare_addresses(*(r['who'] for r in rows)))
    for r in rows:
        r['who'] = name_only(r['who'], names)
    return rows


def words_in(text):
    return set(re.findall(r'[^\W_]+', str(text or '').casefold()))


CHANGE_MARKS = {'− ': 'was', '+ ': 'now'}


def shape_page_change(o, m):
    """A watched page's change (connectors/web_page.py: '− ' a line it had, '+ ' a line it has, the rest around them):
    its site and path in the header, its lines as `changes` ({'kind': 'same', 'was' or 'now', 'text'}) that the viewer
    strikes through or highlights, and as the body (a list row, search) what the page says now, never the marks."""
    page_name = getattr(_connector('web_page.change'), 'page_name', None)
    url = str(m.get('source_url') or '')
    if page_name and url.startswith('https://'):
        o['card'] = {'ref': page_name(url)}
    changes = []
    for line in str(o.get('body') or '').split('\n'):
        mark = CHANGE_MARKS.get(line[:2], 'same')
        changes.append({'kind': mark, 'text': line if mark == 'same' else line[2:]})
    if any(c['kind'] != 'same' for c in changes):
        o['changes'] = changes
        o['body'] = '\n'.join(c['text'] for c in changes if c['kind'] != 'was')


def shape(kind, o, m):
    """Add the viewer's fields to one original (Store.event_views): view, app, format, and per view what it needs,
    following the rules in this module's docstring."""
    view = view_of(kind)
    o['view'] = view
    o['source'] = kind
    o['app'] = app_of(kind, o.get('url'))
    o['format'] = 'markdown' if kind in MARKDOWN_KINDS else 'text'
    title = o.get('title') or ''
    if view == 'email':
        shape_email(o, m, title)
    elif view == 'notification':
        shape_notification(o, m, title)
    elif kind == 'github.notification':
        shape_github(o, m)
    elif kind == 'github.ci':  # "[repo] CI failed on main": the repo in the header, who pushed once
        o['title'] = re.sub(r'^\[[^\]\n]{1,100}\]\s*', '', o['title'])
        actor = str(m.get('from') or '')
        o['card'] = {'ref': str(m.get('repo') or ''), 'author': actor, 'bot': bool(actor and BOT.search(actor))}
        o['body'] = '\n'.join(line for line in o['body'].split('\n') if not (actor and line.strip() == 'By: ' + actor))
        o['from'] = actor
    elif kind == 'web_page.change':
        shape_page_change(o, m)
    elif view == 'card':
        o['body'] = drop_repeats(o['body'], title)
    if transcript_kind(kind) and (turns := transcript_turns(o['body'], m.get('start_at') or o.get('occurred_at'))):
        # a transcript reads as who said what, in turns, at the time of day they said it (chatThreadHTML), never "[0:00:00]"
        o['turns'], o['chat'] = turns, title
    if kind == 'slack.message':  # the title is plain words: a link by its label, an address without "<mailto:…|…>"
        o['title'] = slack_plain(o['title'])
    if kind in ('slack.message', 'whatsapp.message', 'fleet.message'):
        o['body'] = mrkdwn(o['body'], slack=kind != 'whatsapp.message')
        for turn in o.get('turns') or ():
            turn['body'] = mrkdwn(turn['body'], slack=kind != 'whatsapp.message')
    if kind in ('intercom.conversation', 'fleet.intercom'):
        channel = INTERCOM_CHANNELS.get(str(m.get('channel') or '').lower())
        if channel and channel != 'Email':
            o['via'] = channel
        if m.get('subject'):  # the conversation's own title, when it has one; else it reads by the customer's name
            o['subject'] = str(m['subject'])[:300]
    return o
