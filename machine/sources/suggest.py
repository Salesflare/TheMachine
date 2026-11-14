"""Connections, + Add: "Suggested for you", the few sources this Machine would gain most from, each with the signal it
rests on. Only from what the Machine already has: mail from the service (mail_senders.mails_from, as the setup hints count it),
meetings on the calendar with its video link (meet.VIDEO_LINKS), links to it in mail and chat, and a setup started on
the dashboard that didn't finish. No signal, no suggestion: nothing is offered for its own sake, and never a source that
is connected already. Counts only, read on this Machine; nothing leaves it."""
from __future__ import annotations

import datetime as dt
import re

from machine.sources.mail_senders import HINT_MAILS, HINT_SOURCES, mails_from
from meet import VIDEO_LINKS

SHOWN = 3      # at most this many suggestions
ENOUGH = HINT_MAILS  # signals of one kind before it counts: the setup hints' bar for "mails you often"
COUNT_UP_TO = 99
DAYS = 30
MESSAGES_READ = 400  # the latest mail and chat messages looked through for links
# Mail from these senders too, on top of the setup hints' (HINT_SOURCES)
MAIL_DOMAINS = {**{service: domains for service, _, domains in HINT_SOURCES}, 'trello': ('trello.com',), 'shortcut': ('shortcut.com',)}
# The + Add tile a meeting's video link points to
MEETING_TILES = {'zoom': 'zoom', 'meet': 'google_meet', 'teams': 'teams'}
# The + Add tile a link in a message points to: (host, path it starts with)
LINKS = {'google_docs': (('docs.google.com', '/'),), 'docs': (('sharepoint.com', '/'), ('onedrive.live.com', '/'), ('1drv.ms', '/')),
         'github': (('github.com', '/'),), 'trello': (('trello.com', '/c/'), ('trello.com', '/b/')), 'shortcut': (('app.shortcut.com', '/'),),
         'zoom': (('zoom.us', '/j/'),), 'google_meet': (('meet.google.com', '/'),), 'teams': (('teams.microsoft.com', '/l/meetup-join'),)}
LINK_RE = {name: re.compile('|'.join(r'https?://(?:[a-z0-9-]+\.)*' + re.escape(host) + re.escape(path) for host, path in marks), re.I)
           for name, marks in LINKS.items()}
MESSAGE_KINDS = ('gmail.message', 'ms_graph.message', 'outlook.message', 'slack.message', 'teams.message')


def suggestions(db, sources, unfinished=(), now=None):
    """[{name, why, count}] for the + Add tiles in `sources` (onboarding.catalog's, as the dashboard shows them) that
    aren't connected and have a signal: why is 'unfinished' (a setup of it on the dashboard failed: `unfinished` holds
    those tile names), 'meetings' (that many calendar meetings use its video link), 'mail' (that many mails from it in
    DAYS days) or 'links' (that many messages link to it). The strongest signal per tile; a setup that didn't finish
    first, then the most signals. At most SHOWN; [] when nothing has a signal."""
    import timeutil
    open_ = {s['name']: s for s in sources if isinstance(s, dict) and not s.get('connected')}
    if not open_:
        return []
    since = ((now or timeutil.clock()) - dt.timedelta(days=DAYS)).isoformat()
    found = {}

    def note(name, why, count):
        if name in open_ and count >= ENOUGH and count > found.get(name, ('', 0))[1]:
            found[name] = (why, min(count, COUNT_UP_TO))

    for name, domains in MAIL_DOMAINS.items():
        if name in open_:
            note(name, 'mail', mails_from(db, domains, since, COUNT_UP_TO))
    meetings = dict.fromkeys(VIDEO_LINKS, 0)
    rows = db.execute("SELECT metadata FROM events WHERE kind='calendar.event' AND deleted=0 AND occurred_at>=? ORDER BY occurred_at DESC LIMIT 400",
                      (since,)).fetchall()
    for (metadata,) in rows:
        text = str(metadata or '').lower()
        kind = next((k for k, marks in VIDEO_LINKS.items() if any(m in text for m in marks)), None)
        if kind:
            meetings[kind] += 1
    for kind, count in meetings.items():
        note(MEETING_TILES.get(kind, ''), 'meetings', count)
    wanted = [name for name in LINK_RE if name in open_]
    if wanted:
        links = dict.fromkeys(wanted, 0)
        marks = ','.join('?' * len(MESSAGE_KINDS))
        for (body,) in db.execute(f'SELECT body FROM events WHERE kind IN ({marks}) AND deleted=0 AND occurred_at>=? '
                                  'ORDER BY occurred_at DESC LIMIT ?', (*MESSAGE_KINDS, since, MESSAGES_READ)):
            text = body if isinstance(body, str) else ''
            for name in wanted:
                if LINK_RE[name].search(text):
                    links[name] += 1
        for name, count in links.items():
            note(name, 'links', count)
    out = [{'name': name, 'why': 'unfinished', 'count': 0} for name in dict.fromkeys(unfinished) if name in open_]
    ranked = sorted(found.items(), key=lambda item: (-item[1][1], open_[item[0]].get('label') or item[0]))
    out += [{'name': name, 'why': why, 'count': count} for name, (why, count) in ranked if name not in {o['name'] for o in out}]
    return out[:SHOWN]

