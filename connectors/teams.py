"""Microsoft Teams: chats (1:1, group and meeting chats), and with an admin's OK channel messages, meeting transcripts and
Copilot's meeting notes. Read only: GET requests to Microsoft Graph through ms_graph.py, nothing is ever posted. Replies
happen in Teams: each message carries its "Open in Teams" link (source_url).

The sign-in is the one the Machine has for that work address (like connectors/docs.py): Outlook's, when it is
connected, else one of its own (`own_grant`), through the same Microsoft app and token broker. Delegated scopes only,
each asked in its own consent and never by Outlook:

- Chat.Read: the owner's 1:1, group and meeting chats. No admin needed (unless the organization lets no app in
  without one).
- Admin consent, an optional second step that never holds up the chats: Team.ReadBasic.All, Channel.ReadBasic.All and
  ChannelMessage.Read.All (channel messages of the teams the owner is in); OnlineMeetings.Read,
  OnlineMeetingTranscript.Read.All (a meeting's transcript) and OnlineMeetingAiInsight.Read.All (Copilot's notes and
  action items; Microsoft serves them only to a user with a Microsoft 365 Copilot license). Team.ReadBasic.All,
  Channel.ReadBasic.All and OnlineMeetings.Read need no admin by themselves; they come in that step because they are
  only useful with the others.

What reads what, and how often (Graph throttles Teams per app and tenant; every 429 or 503 waits its Retry-After):
- Chats: the chat list ordered by last message is the change feed. Only chats with a message since the last pass are
  read, each from its own cursor (lastModifiedDateTime, so edits and deletions come too). Change notifications would
  need a public endpoint per Machine and Delta for chats is application-only, so neither is used.
- Channels: the channel's own list, ordered by its threads' last activity, with replies expanded, until a thread is
  older than the cursor. Teams and channels are listed again once a day.
- Meetings: a meeting chat's "meeting ended" or "transcript ready" system message queues that meeting. It is looked
  up by its join link, then Copilot's notes and the transcript are read, for up to two days while Microsoft makes them.
  Without them the meeting chat is what there is (it is read as a chat either way). The connection's card says what
  is missing and why (state["missing"]).

Bots, apps and Teams' system messages are left out. The first import reads the last `bootstrap_days` (7); older chat
messages come in as history only (machine/app/history.py), after the first look, one page at a time.

Personal Microsoft accounts have no Teams chats in Graph: work and school accounts only."""
import datetime as dt
from html.parser import HTMLParser
import hashlib
import re
import urllib.parse

KINDS = {'teams.message': 'Teams message', 'teams.notes': 'Teams notes', 'teams.transcript': 'Teams transcript'}
CHAT_SCOPE = 'Chat.Read'
CHANNEL_SCOPES = ('Team.ReadBasic.All', 'Channel.ReadBasic.All', 'ChannelMessage.Read.All')
MEETING_SCOPE, TRANSCRIPT_SCOPE, INSIGHT_SCOPE = 'OnlineMeetings.Read', 'OnlineMeetingTranscript.Read.All', 'OnlineMeetingAiInsight.Read.All'
ADMIN_SCOPES = CHANNEL_SCOPES + (MEETING_SCOPE, TRANSCRIPT_SCOPE, INSIGHT_SCOPE)
SETUP = {
    'label': 'Microsoft Teams',
    'account': {'id': 'teams', 'service': 'teams', 'transport': 'broker', 'boundary': 'work', 'poll_seconds': 300},
    'what': 'Chats, meeting chats and meeting notes from Teams. Reads only.',
    'note': 'Signs in with Microsoft for your work address. Channels and meeting transcripts need your admin’s OK.',
    'ask': [('email', 'Your Microsoft work address')],
    # a hosted Machine: its account page's Teams part signs in (Connect Microsoft Teams), and + Add starts the same
    'account_page': 'teams',
    'hints': {'teams_not_connected': 'Connect Microsoft Teams again',
              'teams_signin_expired': 'Connect Microsoft Teams again',
              'teams_not_granted': 'Connect Microsoft Teams again',
              'teams_work_only': 'Teams needs a work or school account'}}
TEAMS_HOSTS = ('teams.microsoft.com', 'teams.cloud.microsoft', 'teams.live.com')
OVERLAP = dt.timedelta(hours=2)  # each pass rereads this far back: a message edited or sent during the last one
MAX_CHATS = 25          # chats read per run; the rest the next run (a few minutes later)
CHAT_PAGES = 10         # chat list pages per pass (50 each)
MESSAGE_PAGES = 4       # message pages per chat per run (50 each)
MAX_CHANNELS = 10       # channels read per run, in turn
CHANNEL_PAGES = 2
MAX_MEETINGS = 5        # meetings looked at per run
MEETING_DAYS = 2        # a meeting's notes and transcript are looked for this long after it ended
CURSORS_KEEP = 1000
SEEN_KEEP = 500
BODY_CHARS = 40_000
NOTES_CHARS = 40_000
TRANSCRIPT_CHARS = 400_000
MEETING_EVENTS = ('#microsoft.graph.callEndedEventMessageDetail', '#microsoft.graph.callTranscriptEventMessageDetail',
                  '#microsoft.graph.callRecordingEventMessageDetail')
# What the card says is missing (state["missing"]), by part: 'admin' (the admin's OK isn't there), 'blocked' (the
# organization turned Graph access off), 'license' (Copilot's notes need a Microsoft 365 Copilot license)
PARTS = ('channels', 'transcripts', 'notes')


def stamp(value):
    try:
        text = str(value or '').replace('Z', '+00:00')
        text = re.sub(r'(\.\d{6})\d+', r'\1', text)  # Graph sends seven fraction digits
        parsed = dt.datetime.fromisoformat(text)
    except (TypeError, ValueError):
        return None
    return (parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)).astimezone(dt.timezone.utc)


def zulu(moment):
    return moment.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-4] + 'Z'


def teams_link(url):
    parts = urllib.parse.urlsplit(str(url or ''))
    return url if parts.scheme == 'https' and parts.hostname in TEAMS_HOSTS else None


class _Text(HTMLParser):
    """A Teams message's HTML as plain text: paragraphs and line breaks kept, @mentions as the name, emoji as itself."""
    BREAKS = {'br', 'p', 'div', 'li', 'tr', 'h1', 'h2', 'h3', 'blockquote'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []

    def handle_starttag(self, tag, attrs):
        if tag in self.BREAKS:
            self.out.append('\n')
        if tag == 'li':
            self.out.append('- ')
        if tag == 'emoji':
            self.out.append(dict(attrs).get('alt') or '')
        if tag == 'img' and not dict(attrs).get('itemtype', '').endswith('Emoji'):
            self.out.append('[image]')

    def handle_endtag(self, tag):
        if tag in self.BREAKS:
            self.out.append('\n')

    def handle_data(self, data):
        self.out.append(data)


def html_text(body):
    content = str((body or {}).get('content') or '')
    if str((body or {}).get('contentType') or 'html').lower() != 'html':
        return content.strip()
    parser = _Text()
    try:
        parser.feed(content)
        parser.close()
    except Exception:  # noqa: BLE001 - malformed HTML: its text without tags
        return re.sub(r'<[^>]+>', ' ', content).strip()
    text = ''.join(parser.out).replace('\xa0', ' ')
    text = '\n'.join(' '.join(line.split()) for line in text.splitlines())
    return re.sub(r'\n{3,}', '\n\n', text).strip()


def signin(config, account, helpers):
    """The sign-in to call with: the Teams account itself, with Outlook's transport and credential when Outlook is
    connected for that address, else its own sign-in (own_grant, kept under the same address in mail_grants.py).
    Never one a Fleet shares (someone else's)."""
    email = str(account.get('email') or '').strip().lower()
    if not email:
        raise helpers.SourceError('teams_not_connected')
    if account.get('own_grant') and account.get('transport') == 'broker':
        return {'id': account['id'], 'email': email, 'transport': 'broker',
                **{k: account[k] for k in ('connected_at', 'tenant_id') if account.get(k)}}
    found = next((a for a in config.get('accounts', []) if a.get('service') in ('outlook', 'outlook_calendar') and not a.get('shared')
                  and str(a.get('email') or '').lower() == email and a.get('transport') in ('broker', 'graph')), None)
    base = found or (account if account.get('transport') in ('broker', 'graph') else None)
    if not base:
        raise helpers.SourceError('teams_not_connected')
    return {'id': account['id'], 'email': email, 'transport': base['transport'],
            **{k: base[k] for k in ('credential', 'connected_at', 'tenant_id') if base.get(k)}}


class Source:
    def __init__(self, config, account, helpers):
        import ms_graph
        self.api, self.config, self.account, self.helpers = ms_graph, config, account, helpers
        self.signin = signin(config, account, helpers)
        if ms_graph.personal(self.signin):
            raise helpers.SourceError('teams_work_only')
        self.members, self.me, self.calls = {}, None, 0

    def call(self, method, params=None, raw=False):
        self.calls += 1
        try:
            return self.api.call(self.config, self.helpers.credential, self.signin, method, params, raw=raw)
        except self.api.GraphError as error:
            if error.category == 'microsoft_scope_not_granted':
                raise self.helpers.SourceError('teams_not_granted', 403) from None
            if 'signin_expired' in error.category or 'signin_pending' in error.category:
                raise self.helpers.SourceError('teams_signin_expired', error.status, retry_after=error.retry_after) from None
            if error.category in ('microsoft_broker_not_configured', 'microsoft_signin_unreadable') or \
                    (error.category == 'microsoft_broker' and error.status == 404):
                raise self.helpers.SourceError('teams_not_connected') from None
            if error.category in ('timeout', 'microsoft_broker_unreachable', 'microsoft_signin_unreachable'):
                raise self.helpers.SourceError('teams_network') from None
            if error.category in ('unexpected_graph_link', 'repeated_graph_page', 'invalid_json', 'response_too_large'):
                raise self.helpers.SourceError('teams_invalid_page') from None
            raise self.helpers.SourceError('teams_http', error.status, retry_after=error.retry_after) from None

    def pages(self, method, params, most):
        """Up to `most` pages of a list: (items, whether more were left)."""
        seen = set()
        for _ in range(most):
            page = self.call(method, params)
            if not isinstance(page, dict) or not isinstance(page.get('value', []), list):
                raise self.helpers.SourceError('teams_invalid_page')
            yield [i for i in page.get('value') or [] if isinstance(i, dict)]
            link = page.get('@odata.nextLink')
            if not link:
                return
            if link in seen:
                raise self.helpers.SourceError('teams_invalid_page')
            seen.add(link)
            params = {k: v for k, v in params.items() if '{' + k + '}' in self.api.READ[method][1]} | {'$link': link}

    def granted(self):
        try:
            return {str(s).rsplit('/', 1)[-1] for s in self.api.scopes(self.config, self.helpers.credential, self.signin)}
        except self.api.GraphError as error:
            if error.status == 404 or error.category in ('microsoft_broker_not_configured', 'microsoft_signin_unreadable'):
                raise self.helpers.SourceError('teams_not_connected') from None
            if 'not_signed_in' in error.category:
                raise self.helpers.SourceError('teams_not_connected') from None
            raise self.helpers.SourceError('teams_network', error.status) from None

    def whoami(self):
        if self.me is None:
            me = self.call('me', {'$select': 'id,mail,userPrincipalName'})
            if not isinstance(me, dict) or not me.get('id'):
                raise self.helpers.SourceError('teams_invalid_user')
            email = self.api.identity(me)
            if email and email != self.signin['email']:
                raise self.helpers.SourceError('account_identity_mismatch')
            self.me = str(me['id'])
        return self.me

    def chat_members(self, chat_id):
        """{user id: (name, email)} of a chat's people (its members list, Chat.Read), once per run."""
        if chat_id not in self.members:
            found = {}
            for items in self.pages('teams.chat.members', {'chat': chat_id}, 3):
                for m in items:
                    uid = m.get('userId')
                    if uid:
                        found[str(uid)] = (' '.join(str(m.get('displayName') or '').split())[:80], str(m.get('email') or '').strip().lower())
            self.members[chat_id] = found
        return self.members[chat_id]


# ------------------------------------------------------------------------------------------------ messages

def sender(raw):
    """(user id, name) of a person's message, or None for a bot, an app or Teams itself."""
    who = raw.get('from') if isinstance(raw.get('from'), dict) else {}
    user = who.get('user') if isinstance(who.get('user'), dict) else None
    if not user or who.get('application') or who.get('device') or not user.get('id'):
        return None
    return str(user['id']), ' '.join(str(user.get('displayName') or '').split())[:80]


def person_message(raw):
    """Whether a message is a person's own words: not a system event, a bot or app post, or a typing signal."""
    return raw.get('messageType') == 'message' and sender(raw) is not None


def chat_name(chat, members, me):
    topic = ' '.join(str(chat.get('topic') or '').split())
    if topic:
        return topic[:200]
    others = [name for uid, (name, _) in members.items() if uid != me and name]
    return (', '.join(others[:3]) + (f' +{len(others) - 3}' if len(others) > 3 else '')) if others else 'Teams chat'


def message_event(account, chat, raw, members, me):
    """One person's chat or channel message as a teams.message event. chat: {id, kind, name, url, join_url} where id
    is the conversation (a chat, or a channel thread: '<channel id>:<root message id>')."""
    who = sender(raw)
    at = stamp(raw.get('createdDateTime'))
    if not who or not raw.get('id') or not at:
        raise ValueError('not a person message')
    uid, name = who
    body = html_text(raw.get('body'))
    attachments = [a for a in raw.get('attachments') or [] if isinstance(a, dict)]
    if attachments:
        names = [str(a.get('name') or '').strip() for a in attachments if a.get('contentType') == 'reference' and a.get('name')]
        if names:
            body = (body + '\n' if body else '') + '\n'.join('[file] ' + n[:200] for n in names[:10])
    subject = ' '.join(str(raw.get('subject') or '').split())
    if subject:
        body = subject + '\n' + body
    email = (members.get(uid) or ('', ''))[1] or str(((raw.get('from') or {}).get('user') or {}).get('userPrincipalName') or '').lower()
    mine = uid == me
    others = [e for u, (_, e) in members.items() if u != me and e]
    mentions = [m for m in raw.get('mentions') or [] if isinstance(m, dict)]
    link = teams_link(raw.get('webUrl')) or teams_link(chat.get('url'))
    first = body.splitlines()[0] if body else '(message)'
    metadata = {'chat_id': chat['id'], 'chat_kind': chat['kind'], 'chat_name': chat['name'], 'message_id': str(raw['id']),
                'reply_to': str(raw.get('replyToId') or '') or None, 'user_id': uid, 'from': name or email or 'Someone',
                'sender_display': name or None, 'from_email': email or None, 'from_me': mine,
                'to': others[:25] if chat['kind'] != 'channel' else [],
                'mentions_me': any(str(((m.get('mentioned') or {}).get('user') or {}).get('id') or '') == me for m in mentions),
                'importance': raw.get('importance') if raw.get('importance') in ('high', 'urgent') else None,
                'edited_at': raw.get('lastEditedDateTime'), 'source_url': link, 'truncated': len(body) > BODY_CHARS,
                **({'join_url': chat['join_url']} if chat.get('join_url') else {})}
    return {'account_id': account['id'], 'source_id': 'teams:' + hashlib.sha256((chat['id'] + ':' + str(raw['id'])).encode()).hexdigest()[:40],
            'kind': 'teams.message', 'occurred_at': at.isoformat(), 'title': f'{chat["name"]}: {first}'[:1000],
            'body': body[:BODY_CHARS], 'metadata': metadata, 'deleted': bool(raw.get('deletedDateTime'))}


def chat_info(source, chat):
    """{id, kind, name, url, join_url, organizer} for a chat from the chat list or a GET of it."""
    kind = {'oneOnOne': 'oneOnOne', 'group': 'group', 'meeting': 'meeting'}.get(chat.get('chatType'), 'group')
    members = source.chat_members(chat['id'])
    meeting = chat.get('onlineMeetingInfo') if isinstance(chat.get('onlineMeetingInfo'), dict) else {}
    organizer = (meeting.get('organizer') or {}) if isinstance(meeting.get('organizer'), dict) else {}
    return {'id': str(chat['id']), 'kind': kind, 'name': chat_name(chat, members, source.whoami()), 'url': chat.get('webUrl'),
            'join_url': teams_link(meeting.get('joinWebUrl')), 'organizer': str(organizer.get('id') or '') or None}


def read_chat(source, account, chat, since, state):
    """A chat's messages changed since `since`, newest first: (events, newest change seen, meetings it ended)."""
    info = chat_info(source, chat)
    events, newest, meetings = [], since, []
    params = {'chat': info['id'], '$top': 50, '$orderby': 'lastModifiedDateTime desc',
              '$filter': f'lastModifiedDateTime gt {zulu(since)}'}
    skipped = source.helpers.Skips('teams_invalid_message')
    done = False
    for items in source.pages('teams.chat.messages', params, MESSAGE_PAGES):
        for raw in items:
            changed = stamp(raw.get('lastModifiedDateTime')) or stamp(raw.get('createdDateTime'))
            if changed and changed <= since:
                done = True
                break
            newest = max(newest, changed) if changed else newest
            detail = (raw.get('eventDetail') or {}).get('@odata.type') if isinstance(raw.get('eventDetail'), dict) else None
            if info['kind'] == 'meeting' and detail in MEETING_EVENTS and info['join_url']:
                meetings.append({'chat': info['id'], 'url': info['join_url'], 'organizer': info['organizer'],
                                 'ended': (stamp(raw.get('createdDateTime')) or changed).isoformat()})
            if not person_message(raw):
                continue  # Teams' own notices, bots and apps
            event = skipped.take(message_event, account, info, raw, source.members.get(info['id']) or {}, source.whoami())
            if event is not skipped.SKIPPED:
                events.append(event)
        if done:
            break
    skipped.note(state)
    return events, newest, meetings


def active_chats(source, floor):
    """The chats with a message since `floor`, newest first (the list ordered by its last message: Graph's change feed
    for a user's chats). [(chat, last message time)]"""
    out = []
    params = {'$top': 50, '$expand': 'lastMessagePreview', '$orderby': 'lastMessagePreview/createdDateTime desc'}
    for items in source.pages('teams.chats', params, CHAT_PAGES):
        for chat in items:
            last = stamp(((chat.get('lastMessagePreview') or {}) if isinstance(chat.get('lastMessagePreview'), dict) else {}).get('createdDateTime'))
            last = last or stamp(chat.get('lastUpdatedDateTime'))
            if not chat.get('id') or not last:
                continue
            if last < floor:
                return out
            out.append((chat, last))
    return out


# ------------------------------------------------------------------------------------------------ channels

def channel_list(source, state, now):
    """[[team id, channel id, 'Team / channel']], listed again once a day."""
    kept = state.get('channel_list') or {}
    if kept.get('at') and stamp(kept['at']) and stamp(kept['at']) > now - dt.timedelta(days=1):
        return kept.get('items') or []
    items = []
    for teams in source.pages('teams.joined', {'$select': 'id,displayName'}, 5):
        for team in teams:
            for channels in source.pages('teams.channels', {'team': team['id'], '$select': 'id,displayName,membershipType'}, 2):
                items += [[str(team['id']), str(c['id']), f"{' '.join(str(team.get('displayName') or '').split())[:80]} / "
                                                           f"{' '.join(str(c.get('displayName') or '').split())[:80]}"]
                          for c in channels if c.get('id')]
    state['channel_list'] = {'at': now.isoformat(), 'items': items[:300]}
    return state['channel_list']['items']


def thread_activity(root):
    """A channel thread's last change: its root's or any reply's."""
    times = [stamp(root.get('lastModifiedDateTime')), stamp(root.get('createdDateTime'))]
    times += [stamp(r.get('lastModifiedDateTime')) or stamp(r.get('createdDateTime')) for r in root.get('replies') or [] if isinstance(r, dict)]
    times = [t for t in times if t]
    return max(times) if times else None


def read_channel(source, account, team, channel, name, since, state):
    """A channel's threads with activity since `since`: the root and its replies, each thread its own conversation."""
    events, newest = [], since
    skipped = source.helpers.Skips('teams_invalid_message')
    me = source.whoami()
    for items in source.pages('teams.channel.messages', {'team': team, 'channel': channel, '$top': 50, '$expand': 'replies'}, CHANNEL_PAGES):
        stop = False
        for root in items:
            active = thread_activity(root)
            if not active or active <= since:
                stop = True  # sorted by the thread's last activity: the rest is older
                break
            newest = max(newest, active)
            info = {'id': channel + ':' + str(root.get('id')), 'kind': 'channel', 'name': name, 'url': root.get('webUrl')}
            for raw in [root] + [r for r in root.get('replies') or [] if isinstance(r, dict)]:
                changed = stamp(raw.get('lastModifiedDateTime')) or stamp(raw.get('createdDateTime'))
                if not person_message(raw) or not changed or changed <= since:
                    continue
                event = skipped.take(message_event, account, info, raw, {}, me)
                if event is not skipped.SKIPPED:
                    events.append(event)
        if stop:
            break
    skipped.note(state)
    return events, newest


# ------------------------------------------------------------------------------------------------ meetings

def vtt_text(vtt):
    """A Teams WebVTT transcript as 'Speaker: words' lines, a speaker's run joined."""
    lines = []
    for block in re.split(r'\r?\n\r?\n', vtt):
        for line in block.splitlines():
            line = line.strip()
            if not line or '-->' in line or line.startswith(('WEBVTT', 'NOTE')) or re.fullmatch(r'[0-9a-f-]{8,}(/\d+-\d+)?|\d+', line):
                continue
            found = re.fullmatch(r'<v ([^>]{1,80})>(.*?)(?:</v>)?', line)
            who, said = (found[1].strip(), found[2].strip()) if found else (None, re.sub(r'</?v[^>]*>', '', line).strip())
            if not said:
                continue
            if lines and lines[-1][0] == who:
                lines[-1][1].append(said)
            else:
                lines.append((who, [said]))
    return '\n'.join((f'{who}: ' if who else '') + ' '.join(said) for who, said in lines)


def insight_text(found):
    """Copilot's meeting notes and action items (callAiInsight) as plain text."""
    parts = []
    for note in found.get('meetingNotes') or []:
        if not isinstance(note, dict):
            continue
        parts.append(' '.join(str(note.get('title') or '').split()) + ('\n' + str(note.get('text')).strip() if note.get('text') else ''))
        for sub in note.get('subpoints') or []:
            if isinstance(sub, dict):
                parts.append('- ' + ' '.join(str(sub.get('title') or '').split()) + (': ' + str(sub.get('text')).strip() if sub.get('text') else ''))
    steps = []
    for item in found.get('actionItems') or []:
        if isinstance(item, dict) and (item.get('title') or item.get('text')):
            owner = ' '.join(str(item.get('ownerDisplayName') or '').split())
            steps.append('- ' + ' '.join(str(item.get('title') or item.get('text')).split()) + (f' ({owner})' if owner else ''))
    if steps:
        parts.append('Action items\n' + '\n'.join(steps[:40]))
    return '\n\n'.join(p for p in parts if p.strip())


def meeting_events(source, account, item, granted, missing):
    """What there is of one ended meeting: Copilot's notes and its transcript, each once. Returns (events, whether to
    look again later). Sets missing['transcripts'] and missing['notes'] when Microsoft says no."""
    helpers = source.helpers
    events = []
    if not item.get('meeting'):
        url = item['url'].replace("'", "''")
        found = source.call('teams.meetings', {'$filter': f"JoinWebUrl eq '{url}'"})
        meetings = [m for m in (found or {}).get('value') or [] if isinstance(m, dict) and m.get('id')]
        if not meetings:
            return [], False  # not one this sign-in may see (another organization's, say): the meeting chat is what there is
        m = meetings[0]
        organizer = ((m.get('participants') or {}).get('organizer') or {}) if isinstance(m.get('participants'), dict) else {}
        item.update(meeting=str(m['id']), subject=' '.join(str(m.get('subject') or '').split())[:300] or 'Teams meeting',
                    start=m.get('startDateTime'), end=m.get('endDateTime'), host=str(organizer.get('upn') or '').lower() or None,
                    organizer=item.get('organizer') or str(((organizer.get('identity') or {}).get('user') or {}).get('id') or '') or None)
    begun = stamp(item.get('start')) or stamp(item['ended'])
    span = {'start_at': begun.isoformat(), **({'end_at': stamp(item['end']).isoformat()} if stamp(item.get('end')) else {})}
    base = {'meeting_id': hashlib.sha256(item['meeting'].encode()).hexdigest()[:32], 'host_email': item.get('host'),
            'thread_id': item['chat'], **span, **({'source_url': teams_link(item['url'])} if teams_link(item['url']) else {})}
    again = False
    if INSIGHT_SCOPE in granted and not item.get('notes_done'):
        try:  # the signed-in user's own view of the meeting (delegated): their id in the path
            listed = source.call('teams.insights', {'user': source.whoami(), 'meeting': item['meeting']})
            insights = [i for i in (listed or {}).get('value') or [] if isinstance(i, dict) and i.get('id')]
            if insights:
                found = source.call('teams.insight', {'user': source.whoami(), 'meeting': item['meeting'], 'insight': insights[-1]['id']})
                body = insight_text(found if isinstance(found, dict) else {})
                if body:
                    steps = [' '.join(str(a.get('title') or a.get('text') or '').split()) for a in (found.get('actionItems') or []) if isinstance(a, dict)]
                    events.append({'account_id': account['id'], 'source_id': 'teams-notes:' + base['meeting_id'], 'kind': 'teams.notes',
                                   'occurred_at': begun.isoformat(), 'title': item['subject'], 'body': body[:NOTES_CHARS], 'deleted': False,
                                   'metadata': {**base, 'next_steps': [s for s in steps if s][:40], 'truncated': len(body) > NOTES_CHARS}})
                    item['notes_done'] = True
            else:
                again = True  # Copilot makes them a while after the meeting
            missing.pop('notes', None)
        except helpers.SourceError as error:
            if error.status not in (403, 404):
                raise
            if error.status == 403:
                missing['notes'] = 'license'  # granted, refused: Microsoft serves them only with a Copilot license
            item['notes_done'] = True
    if TRANSCRIPT_SCOPE in granted and not item.get('transcript_done'):
        try:
            listed = source.call('teams.transcripts', {'meeting': item['meeting']})
            transcripts = [t for t in (listed or {}).get('value') or [] if isinstance(t, dict) and t.get('id')]
            if transcripts:
                text = vtt_text(source.call('teams.transcript.content', {'meeting': item['meeting'], 'transcript': transcripts[-1]['id'],
                                                                        '$format': 'text/vtt'}, raw=True).decode('utf-8', 'replace'))
                if text:
                    events.append({'account_id': account['id'], 'source_id': 'teams-transcript:' + base['meeting_id'], 'kind': 'teams.transcript',
                                   'occurred_at': begun.isoformat(), 'title': item['subject'], 'body': text[:TRANSCRIPT_CHARS], 'deleted': False,
                                   'metadata': {**base, 'truncated': len(text) > TRANSCRIPT_CHARS}})
                item['transcript_done'] = True
            else:
                again = True  # none yet, or transcription was off: looked for again until MEETING_DAYS
            missing.pop('transcripts', None)
        except helpers.SourceError as error:
            if error.status not in (403, 404):
                raise
            if error.status == 403:
                missing['transcripts'] = 'blocked'  # granted, refused: the organization turned transcript access off
            item['transcript_done'] = True
    return events, again


# ------------------------------------------------------------------------------------------------ sync

def missing_by_scope(granted, missing):
    """The parts the admin's OK would add, kept with what Microsoft refused (license, blocked)."""
    out = {k: v for k, v in missing.items() if k in PARTS and v != 'admin'}
    if not set(CHANNEL_SCOPES) <= granted:
        out['channels'] = 'admin'
    if not {MEETING_SCOPE, TRANSCRIPT_SCOPE} <= granted:
        out['transcripts'] = 'admin'
    if not {MEETING_SCOPE, INSIGHT_SCOPE} <= granted:
        out['notes'] = 'admin'
    return out


def sync(store, config, account, helpers):
    source = Source(config, account, helpers)
    state = dict(store.checkpoint(account['id']) or {})
    now = stamp(helpers.now())
    granted = source.granted()
    if CHAT_SCOPE not in granted and 'Chat.ReadWrite' not in granted:
        raise helpers.SourceError('teams_not_connected', 403)
    source.whoami()
    days = max(1, min(30, int(config.get('bootstrap_days', 7) or 7)))
    first = not state.get('since')
    floor = (stamp(state['since']) - OVERLAP) if state.get('since') else now - dt.timedelta(days=days)
    cursors = dict(state.get('cursors') or {})
    missing = missing_by_scope(granted, dict(state.get('missing') or {}))
    meetings = list(state.get('meetings') or [])
    count = 0
    if 'queue' not in state:
        listed = active_chats(source, floor)
        state.update(queue=[c['id'] for c, _ in listed], pass_at=now.isoformat())
        cache = {c['id']: c for c, _ in listed}
    else:
        cache = {}
    queue = list(state['queue'])
    for chat_id in queue[:MAX_CHATS]:
        chat = cache.get(chat_id) or source.call('teams.chat', {'chat': chat_id})
        since = max(floor, stamp(cursors.get(chat_id)) - OVERLAP) if stamp(cursors.get(chat_id)) else floor
        events, newest, ended = read_chat(source, account, chat, since, state)
        cursors[chat_id] = newest.isoformat()
        for item in ended:
            if not any(m['chat'] == item['chat'] and m['url'] == item['url'] for m in meetings):
                meetings.append(item)
        queue.remove(chat_id)
        if len(cursors) > CURSORS_KEEP:
            cursors = dict(sorted(cursors.items(), key=lambda kv: kv[1])[-CURSORS_KEEP:])
        state.update(queue=queue, cursors=cursors, meetings=meetings[-50:])
        store.commit_page(account['id'], state, events)
        count += len(events)
    more = bool(queue)
    if not more:
        state['since'] = state.pop('pass_at', now.isoformat())
        state.pop('queue', None)
        # channels, with the admin's OK: in turn, a few a run
        if 'channels' not in missing:
            try:
                channels = channel_list(source, state, now)
                ccursors, turn = dict(state.get('channel_cursors') or {}), int(state.get('channel_turn') or 0)
                for n in range(min(MAX_CHANNELS, len(channels))):
                    team, channel, name = channels[(turn + n) % len(channels)]
                    since = max(now - dt.timedelta(days=days), stamp(ccursors.get(channel)) - OVERLAP) if stamp(ccursors.get(channel)) \
                        else now - dt.timedelta(days=days)
                    events, newest = read_channel(source, account, team, channel, name, since, state)
                    ccursors[channel] = newest.isoformat()
                    state.update(channel_cursors=ccursors, channel_turn=(turn + n + 1) % max(1, len(channels)))
                    store.commit_page(account['id'], state, events)
                    count += len(events)
                more = more or len(channels) > MAX_CHANNELS and not first
            except helpers.SourceError as error:
                if error.status != 403:
                    raise
                missing['channels'] = 'admin'
        # meetings: notes and transcript, while Microsoft makes them
        if MEETING_SCOPE in granted and ({TRANSCRIPT_SCOPE, INSIGHT_SCOPE} & granted):
            kept, looked = [], 0
            for n, item in enumerate(meetings):
                ended = stamp(item.get('ended'))
                if not ended or ended < now - dt.timedelta(days=MEETING_DAYS):
                    continue  # too old: the meeting chat is what there is
                if looked >= MAX_MEETINGS or item.get('next') and stamp(item['next']) and stamp(item['next']) > now:
                    kept.append(item)
                    continue
                looked += 1
                events, again = meeting_events(source, account, item, granted, missing)
                count += len(events)
                if again:
                    item['next'] = (now + dt.timedelta(minutes=30)).isoformat()
                    kept.append(item)
                state.update(meetings=kept + meetings[n + 1:], missing=missing)
                store.commit_page(account['id'], state, events)
            meetings = kept
    state.update(meetings=meetings[-50:], missing=missing, mode='incremental', coverage_complete=not more,
                 coverage='Teams chats caught up.' if not more else 'Teams chats are still being read.')
    store.commit_page(account['id'], state, [])
    return {'mode': 'incremental', 'events': count, 'more': more, 'calls': source.calls}


def check(config, account, helpers):
    """A real read that stores nothing: Chat.Read is granted, the sign-in is the owner's own, and the chat list reads."""
    source = Source(config, account, helpers)
    granted = source.granted()
    if CHAT_SCOPE not in granted and 'Chat.ReadWrite' not in granted:
        raise helpers.SourceError('teams_not_connected', 403)
    source.whoami()
    next(source.pages('teams.chats', {'$top': 1}, 1))
    return None


# ------------------------------------------------------------------------------------------------ history

def history_page(config, account, helpers, state, upper, target):
    """One small step of older messages, kept as history (machine/app/history.py), newest first, from `upper` back to
    `target`: first the list of chats, then one page of 50 per step; after the chats, with the admin's OK the live sync
    has too, the channels of the teams the owner is in (the same list it reads), one page of threads per step. Returns
    (events, done). state holds only chat and channel ids and Graph's next link. A 429 or 503 raises with its
    Retry-After, and all history rests (machine/app/history.py history_rest)."""
    source = Source(config, account, helpers)
    upper, target = stamp(upper), stamp(target)
    if 'chats' not in state:
        chats = []
        for items in source.pages('teams.chats', {'$top': 50}, CHAT_PAGES * 2):
            chats += [str(c['id']) for c in items if c.get('id')]
        state.update(chats=chats, link=None)
        return [], False
    if state['chats']:
        return history_chat(source, account, state, upper, target), False
    if 'channels' not in state:
        state.update(channels=history_channels(source), link=None)
        return [], not state['channels']
    if not state['channels']:
        return [], True
    return history_channel(source, account, state, upper, target), not state['channels']


def history_chat(source, account, state, upper, target):
    chat_id = state['chats'][0]
    chat = source.call('teams.chat', {'chat': chat_id})
    info = chat_info(source, chat)
    params = {'chat': chat_id, '$top': 50, '$orderby': 'createdDateTime desc', '$filter': f'createdDateTime lt {zulu(upper)}'}
    if state.get('link'):
        params = {'chat': chat_id, '$link': state['link']}
    page = source.call('teams.chat.messages', params)
    events, old = [], False
    for raw in (page or {}).get('value') or []:
        at = stamp(raw.get('createdDateTime')) if isinstance(raw, dict) else None
        if not at or at < target:
            old = True
            continue
        if person_message(raw) and not raw.get('deletedDateTime'):
            try:
                events.append(message_event(account, info, raw, source.members.get(chat_id) or {}, source.whoami()))
            except (ValueError, KeyError, TypeError):
                continue
    link = (page or {}).get('@odata.nextLink')
    if old or not link:
        state['chats'] = state['chats'][1:]
        state['link'] = None
    else:
        state['link'] = link
    return events


def history_channels(source):
    """[[team id, channel id, 'Team / channel']] of the teams the owner is in, only when the live sync reads channels too
    (the admin's OK): never more than it reads. Without it, or refused, none."""
    if not set(CHANNEL_SCOPES) <= source.granted():
        return []
    try:
        return channel_list(source, {}, dt.datetime.now(dt.timezone.utc))
    except source.helpers.SourceError as error:
        if error.status != 403:
            raise
        return []


def history_channel(source, account, state, upper, target):
    """One page of a channel's threads (sorted by their last activity, replies with them): the messages from `target`
    up to `upper` (newer ones are the live sync's). A thread last active before `target` ends the channel."""
    team, channel, name = state['channels'][0]
    params = {'team': team, 'channel': channel, '$top': 50, '$expand': 'replies'}
    if state.get('link'):
        params = {'team': team, 'channel': channel, '$link': state['link']}
    try:
        page = source.call('teams.channel.messages', params)
    except source.helpers.SourceError as error:
        if error.status not in (403, 404):
            raise
        page = {}  # gone, or no longer the owner's: on to the next one
    events, old, me = [], False, source.whoami()
    for root in (page or {}).get('value') or []:
        if not isinstance(root, dict):
            continue
        active = thread_activity(root)
        if not active or active < target:
            old = True
            break
        info = {'id': channel + ':' + str(root.get('id')), 'kind': 'channel', 'name': name, 'url': root.get('webUrl')}
        for raw in [root] + [r for r in root.get('replies') or [] if isinstance(r, dict)]:
            at = stamp(raw.get('createdDateTime'))
            if not at or not target <= at < upper or not person_message(raw) or raw.get('deletedDateTime'):
                continue
            try:
                events.append(message_event(account, info, raw, {}, me))
            except (ValueError, KeyError, TypeError):
                continue
    link = (page or {}).get('@odata.nextLink')
    if old or not link:
        state['channels'] = state['channels'][1:]
        state['link'] = None
    else:
        state['link'] = link
    return events
