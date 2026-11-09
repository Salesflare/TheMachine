"""Routine suggestions from what the owner does (docs/help/routines.md#from-what-you-do): read-only, plain code, no model.

OpenClaw jobs (routine_imports.py) only help someone who had them. This looks at the owner's own activity on this
Machine for work that comes back on a rhythm, so a hosted Machine gets suggestions too:

- ask: the same ask, over and over (a to-do the owner made, or what they wrote in a to-do's chat), like "sum up the
  open support tickets" every Monday;
- sent: a new mail (no reply) the owner sends on a rhythm with the same subject to the same people, like a weekly report;
- mail: newsletters and update mails (List-Unsubscribe or List-Id) that keep coming from the same senders, every week;
  promotions apart from the rest;
- slack: a busy Slack channel others write in every week, where the owner mostly reads;
- forward: mails the owner forwards one by one to the same one person, week after week, like school and club mails to
  a partner (a weekly digest for them would save the forwarding);
- reply: the same request answered on a rhythm: replies to the same person on the same subject (without dates and
  numbers), one per thread, weekly to quarterly, like a monthly timesheet approval.

Each candidate needs at least MIN_TIMES occurrences on a recognizable rhythm, the latest of them recent (forwards: at
least MIN_FORWARDS in FORWARD_WEEKS weeks, in three different weeks). Forwards and replies stay in the account they
were sent from: a candidate is one account's (`account`), so Work and Personal never mix. Nothing here
judges what it means: the routines worker hands the strongest new candidate to one sorting run a day (routines_app.py),
where the model says whether it is a routine worth having (with a real preview run), a recurring to-do, or nothing. A
to-do the owner closes on a rhythm is recurring.py's (find_offers), never a candidate here.

Everything stays on the Machine: candidates are computed from its own database each time and only their evidence goes
into the owner's own model run. `why` is what the suggestion says about its evidence, as numbers (the dashboard
words it in the owner's language), plus, for forwards and replies, who they went to (`to`: a first name or address)."""
import datetime as dt
import hashlib
import json
import re
from collections import Counter

import recurring

LOOK_DAYS = 120  # how far back asks and sent mail are looked at
DIGEST_WEEKS = 6  # how far back newsletters and channels are looked at
MIN_TIMES = 3
SNIP = 200  # characters of one piece of evidence
EVIDENCE = 6  # pieces of evidence per candidate
SAME = 0.5  # word overlap (Jaccard) at which two asks are taken as the same ask; the model judges the rest
SLACK_WEEK = 10  # messages by others that make a channel's week busy
OWN_SHARE = 0.2  # a channel where the owner writes more than this is a conversation, not one to sum up
DIGEST_AT = '08:00'
DIGEST_DAY = 4  # Friday
FORWARD_WEEKS = 6  # how far back forwards are looked at
MIN_FORWARDS = 5  # forwards to one person in FORWARD_WEEKS that make a strong pattern (in MIN_TIMES different weeks)
REPLY_DAYS = 290  # how far back replies are looked at: three quarters
KINDS = ('ask', 'forward', 'sent', 'reply', 'slack', 'mail')  # strongest first: the owner's own manual work says most
_RE = re.compile(r'^(?:(?:re|fw|fwd|aw|wg|tr|rv|r)\s*:\s*)+', re.I)
_FWD = re.compile(r'^\s*(?:fwd?|wg|tr|rv|doorst|enc|i)\s*:', re.I)
_FWD_BODY = re.compile(r'-{3,}\s*(?:forwarded message|original message|doorgestuurd bericht|weitergeleitete nachricht|message transféré|'
                       r'mensaje reenviado|messaggio inoltrato|mensagem encaminhada)|^begin forwarded message:', re.I | re.M)
_FROM_LINE = re.compile(r'^\s*\**(?:from|van|von|de|da)\s*:\**\s*(.+)$', re.I | re.M)
_WORD = re.compile(r'[^\W\d_]{3,}')


def words(text):
    """An ask's words, for grouping: letters only, no dates, numbers or weekdays (recurring.title_key)."""
    return set(_WORD.findall(recurring.title_key(text)))


def _key(*parts):
    return hashlib.sha256('\x1f'.join(map(str, parts)).encode()).hexdigest()[:16]


def _local(stamp, tz):
    try:
        moment = dt.datetime.fromisoformat(str(stamp).replace('Z', '+00:00'))
    except ValueError:
        return None
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=dt.timezone.utc)
    return moment.astimezone(tz)


def _meta(value):
    if isinstance(value, dict):
        return value
    try:
        got = json.loads(value or '{}')
    except (TypeError, ValueError):
        return {}
    return got if isinstance(got, dict) else {}


def _rule_of(days):
    """A rhythm in these dates (oldest first, one per day): daily, weekdays, or recurring.rhythm_of's weekly, every two
    weeks or monthly, or quarterly. None when they don't keep one."""
    gaps = [(b - a).days for a, b in zip(days, days[1:])]
    if len(days) >= MIN_TIMES and all(85 <= g <= 98 for g in gaps):
        return {'unit': 'month', 'n': 3}
    if len(days) >= 5 and all(g == 1 for g in gaps):
        return {'unit': 'day', 'n': 1}
    if len(days) >= 5 and all(d.weekday() < 5 for d in days) and all(g == 1 or (g == 3 and a.weekday() == 4) for a, g in zip(days, gaps)):
        return {'unit': 'weekday', 'n': 1}
    return recurring.rhythm_of(days)


_LATE = {'day': 3, 'weekday': 4, 'week': 10, 'month': 36}


def rhythm(moments, today):
    """The rhythm the latest of these local moments keep: (rule, the dates in it, oldest first) or None. The longest
    run of dates up to the newest that keeps one, at least MIN_TIMES, and the newest recent enough to still hold."""
    days = sorted({m.date() for m in moments})
    for size in range(len(days), MIN_TIMES - 1, -1):
        tail = days[-size:]
        rule = _rule_of(tail)
        if rule:
            late = _LATE[rule['unit']] + (7 if rule['unit'] == 'week' and rule['n'] == 2 else 0) + (61 if rule == {'unit': 'month', 'n': 3} else 0)
            return (rule, tail) if (today - tail[-1]).days <= late else None
    return None


def _when(rule, tail, moments, today):
    """(anchor, at) for a rhythm: on the weekday or day of the month it keeps, an hour before the earliest time of day
    the owner did it, so the result is there first (never before 06:00)."""
    if rule['unit'] in ('week', 'month'):
        weekday = Counter(d.weekday() for d in tail).most_common(1)[0][0]
        anchor = (recurring.anchor_for(rule, today, weekday=weekday) if rule['unit'] == 'week'
                  else recurring.anchor_for(rule, today, monthday=Counter(d.day for d in tail).most_common(1)[0][0]))
    else:
        anchor = recurring.anchor_for(rule, today)
    times = [m for m in moments if m.date() in set(tail)]
    hour = max(6, min(m.hour for m in times) - 1) if times else 8
    return anchor, f'{hour:02d}:00'


def _line(moment, text):
    return f"{moment.strftime('%a %Y-%m-%d %H:%M')}: {' '.join(str(text or '').split())[:SNIP]}"


def asks(db, today, tz):
    """The owner's own asks on a rhythm: to-dos they made and what they wrote in to-do chats, grouped by their words."""
    since = (today - dt.timedelta(days=LOOK_DAYS)).isoformat()
    found = []
    try:
        found += [(r['created_at'], r['text']) for r in db.execute(
            "SELECT created_at,coalesce(nullif(owner_words,''),title) AS text FROM suggestions WHERE origin='owner' AND created_at>=? "
            'ORDER BY created_at', (since,))]
    except Exception:
        pass  # an older database without owner to-dos' words
    found += [(r['created_at'], r['feedback']) for r in db.execute(
        "SELECT created_at,feedback FROM decisions WHERE choice='other' AND source IN ('dashboard','telegram') AND feedback!='' "
        'AND created_at>=? ORDER BY created_at', (since,))]
    groups = []  # [(words of the latest ask, [(moment, text)])]
    for stamp, text in sorted(found, key=lambda x: str(x[0])):
        moment, said = _local(stamp, tz), words(text)
        if not moment or len(said) < 2:
            continue
        for i, (have, items) in enumerate(groups):
            if len(have & said) / len(have | said) >= SAME:
                items.append((moment, text))
                groups[i] = (said, items)
                break
        else:
            groups.append((said, [(moment, text)]))
    out = []
    for _, items in groups:
        got = rhythm([m for m, _ in items], today)
        if not got:
            continue
        rule, tail = got
        moments = [m for m, _ in items]
        anchor, at = _when(rule, tail, moments, today)
        kept = [(m, t) for m, t in items if m.date() in set(tail)]
        out.append({'key': 'pattern:ask:' + _key(*sorted(words(items[0][1]))), 'kind': 'ask', 'rule': rule, 'anchor': anchor, 'at': at,
                    'count': len(tail), 'name': ' '.join(str(kept[-1][1]).split())[:80],
                    'titles': sorted({recurring.title_key(t) for _, t in kept}),
                    'evidence': [_line(m, t) for m, t in kept[-EVIDENCE:]], 'why': {'kind': 'ask', 'n': len(tail)}})
    return out


def _addresses(value):
    return sorted({a.lower() for a in re.findall(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+', str(value or ''))})


def sent(db, today, tz):
    """New mails the owner sends on a rhythm: the same subject (without dates and numbers) to the same people."""
    since = (today - dt.timedelta(days=LOOK_DAYS)).isoformat()
    groups = {}
    for r in db.execute("SELECT id,occurred_at,title,body,metadata FROM events WHERE kind='gmail.message' AND deleted=0 AND occurred_at>=? "
                        "AND EXISTS(SELECT 1 FROM json_each(json_extract(events.metadata,'$.labels')) WHERE value='SENT') ORDER BY occurred_at",
                        (since,)):
        m = _meta(r['metadata'])
        subject = _RE.sub('', str(r['title'] or '')).strip()
        if m.get('in-reply-to') or _RE.match(str(r['title'] or '')) or _FWD.match(str(r['title'] or '')):
            continue  # a reply answers someone, a forward passes mail on (reply, forward): not a report of the owner's own
        topic, to = recurring.title_key(subject), tuple(_addresses(m.get('to')) + _addresses(m.get('cc')))
        moment = _local(r['occurred_at'], tz)
        if len(topic) >= 4 and to and moment:
            groups.setdefault((topic, to), []).append((moment, subject, r['body'], r['id']))
    out = []
    for (topic, to), items in groups.items():
        got = rhythm([i[0] for i in items], today)
        if not got:
            continue
        rule, tail = got
        anchor, at = _when(rule, tail, [i[0] for i in items], today)
        kept = [i for i in items if i[0].date() in set(tail)]
        latest = kept[-1]
        body = str(latest[2] or '').split('[Quoted earlier messages', 1)[0].strip()
        out.append({'key': 'pattern:sent:' + _key(topic, *to), 'kind': 'sent', 'rule': rule, 'anchor': anchor, 'at': at, 'count': len(tail),
                    'name': latest[1][:80], 'titles': [topic],
                    'evidence': [f'To {len(to)} {"person" if len(to) == 1 else "people"}: {", ".join(to[:4])}']
                    + [_line(m, s) + f' (event {i})' for m, s, _, i in kept[-EVIDENCE:]]
                    + [f'The latest one, as written: {" ".join(body.split())[:800]}'],
                    'why': {'kind': 'sent', 'n': len(tail)}})
    return out


def _person(value):
    """(address, first name or the address) of the one person in a To line."""
    text = str(value or '')
    address = (_addresses(text) or [''])[0]
    name = re.sub(r'\s*<[^>]*>\s*', '', text).strip(' "\'')
    first = name.split()[0].strip(',') if name and '@' not in name else ''
    return address, first[:40] or address


def _sent_mail(db, since):
    """The owner's sent mail since a date: (row, metadata, subject) per mail, oldest first."""
    for r in db.execute("SELECT id,account_id,occurred_at,title,body,metadata FROM events WHERE kind='gmail.message' AND deleted=0 "
                        "AND occurred_at>=? AND EXISTS(SELECT 1 FROM json_each(json_extract(events.metadata,'$.labels')) WHERE value='SENT') "
                        'ORDER BY occurred_at', (since,)):
        yield r, _meta(r['metadata']), str(r['title'] or '')


def forward(db, today, tz):
    """Mails the owner forwards, one by one, to the same one person: at least MIN_FORWARDS in FORWARD_WEEKS weeks, in
    at least MIN_TIMES different weeks, the latest in the last ten days. Per account (Work and Personal apart), never
    to the owner's own address. The rhythm is weekly, on the day they forward most."""
    since = (today - dt.timedelta(weeks=FORWARD_WEEKS)).isoformat()
    groups = {}
    for r, m, title in _sent_mail(db, since):
        body = str(r['body'] or '')
        if not (_FWD.match(title) or (not _RE.match(title) and _FWD_BODY.search(body))):
            continue
        to = _addresses(m.get('to')) + _addresses(m.get('cc'))
        own = set(_addresses(m.get('from')))
        moment = _local(r['occurred_at'], tz)
        if len(to) != 1 or to[0] in own or not moment:
            continue  # a group or the owner's own address: not one person they pass mail on to
        quoted = _FWD_BODY.split(body, 1)
        source = _FROM_LINE.search(quoted[1]) if len(quoted) > 1 else None
        source = re.sub(r'\s*<[^>]*>\s*', '', source.group(1)).strip(' "*') if source else ''
        subject = _FWD.sub('', _RE.sub('', title)).strip() or title
        groups.setdefault((r['account_id'], to[0]), []).append((moment, subject, source[:60], r['id'], m.get('to')))
    out = []
    for (account, address), items in groups.items():
        weeks = {m.isocalendar()[:2] for m, *_ in items}
        if len(items) < MIN_FORWARDS or len(weeks) < MIN_TIMES or (today - items[-1][0].date()).days > 10:
            continue
        _, name = _person(items[-1][4])
        rule = {'unit': 'week', 'n': 1}
        weekday = Counter(m.weekday() for m, *_ in items).most_common(1)[0][0]
        span = max(2, -(-((items[-1][0].date() - items[0][0].date()).days + 1) // 7))
        out.append({'key': 'pattern:forward:' + _key(account, address), 'kind': 'forward', 'account': account, 'rule': rule,
                    'anchor': recurring.anchor_for(rule, today + dt.timedelta(days=1), weekday=weekday), 'at': DIGEST_AT,
                    'count': len(items), 'name': f'Forwards to {name}'[:80], 'titles': [],
                    'evidence': [f'All forwarded to the same one person: {name} <{address}>, {len(items)} times in {span} weeks, from account {account}']
                    + [_line(m, s) + (f' (originally from {src})' if src else '') + f' (event {i})' for m, s, src, i, _ in items[-EVIDENCE * 2:]],
                    'why': {'kind': 'forward', 'n': len(items), 'weeks': span, 'to': name}})
    return out


def reply(db, today, tz):
    """The same request answered on a rhythm: the owner's replies to the same one person on the same subject (without
    dates and numbers), the first reply per thread, weekly to quarterly (REPLY_DAYS back). Per account."""
    since = (today - dt.timedelta(days=REPLY_DAYS)).isoformat()
    groups, threads = {}, set()
    for r, m, title in _sent_mail(db, since):
        if _FWD.match(title) or not (m.get('in-reply-to') or _RE.match(title)):
            continue
        thread = (r['account_id'], str(m.get('thread_id') or title))
        to = _addresses(m.get('to'))
        topic = recurring.title_key(_RE.sub('', title))
        moment = _local(r['occurred_at'], tz)
        if thread in threads or len(to) != 1 or len(topic) < 4 or not moment:
            continue
        threads.add(thread)
        groups.setdefault((r['account_id'], to[0], topic), []).append((moment, _RE.sub('', title).strip(), r['id'], m.get('to')))
    out = []
    for (account, address, topic), items in groups.items():
        got = rhythm([i[0] for i in items], today)
        if not got:
            continue
        rule, tail = got
        anchor, at = _when(rule, tail, [i[0] for i in items], today)
        kept = [i for i in items if i[0].date() in set(tail)]
        _, name = _person(kept[-1][3])
        out.append({'key': 'pattern:reply:' + _key(account, address, topic), 'kind': 'reply', 'account': account, 'rule': rule,
                    'anchor': anchor, 'at': at, 'count': len(tail), 'name': kept[-1][1][:80], 'titles': [topic],
                    'evidence': [f'Replies to the same one person: {name} <{address}>, the same request each time, from account {account}']
                    + [_line(m, s) + f' (event {i})' for m, s, i, _ in kept[-EVIDENCE:]],
                    'why': {'kind': 'reply', 'n': len(tail), 'to': name}})
    return out


def mail(db, today, tz):
    """Newsletters and update mails that keep coming: per sender, mail in at least MIN_TIMES of the last DIGEST_WEEKS
    weeks; one candidate for promotions, one for the rest, each with at least two such senders (or one that writes
    daily)."""
    since = (today - dt.timedelta(weeks=DIGEST_WEEKS)).isoformat()
    senders = {}
    for r in db.execute("SELECT id,occurred_at,title,metadata FROM events WHERE kind='gmail.message' AND deleted=0 AND occurred_at>=? "
                        "AND NOT EXISTS(SELECT 1 FROM json_each(json_extract(events.metadata,'$.labels')) WHERE value IN ('SENT','SPAM','TRASH')) "
                        'ORDER BY occurred_at', (since,)):
        m = _meta(r['metadata'])
        if not (m.get('list_unsubscribe') or m.get('list_id')):
            continue
        sender = (_addresses(m.get('from')) or [''])[0]
        moment = _local(r['occurred_at'], tz)
        if not sender or not moment:
            continue
        labels = set(m.get('labels') or ())
        name = re.sub(r'\s*<[^>]*>\s*', '', str(m.get('from') or '')).strip(' "') or sender
        s = senders.setdefault(sender, {'name': name[:60], 'items': [], 'unread': 0, 'promo': 0})
        s['items'].append((moment, str(r['title'] or ''), r['id']))
        s['unread'] += 'UNREAD' in labels
        s['promo'] += 'CATEGORY_PROMOTIONS' in labels
    out = []
    for group in ('news', 'promo'):
        steady = []
        for address, s in senders.items():
            if (s['promo'] * 2 > len(s['items'])) != (group == 'promo'):
                continue
            weeks = {m.isocalendar()[:2] for m, _, _ in s['items']}
            if len(s['items']) >= MIN_TIMES and len(weeks) >= MIN_TIMES and (today - s['items'][-1][0].date()).days <= 10:
                steady.append((address, s))
        if not steady or (len(steady) < 2 and len(steady[0][1]['items']) < 5 * DIGEST_WEEKS):
            continue
        steady.sort(key=lambda x: -len(x[1]['items']))
        rule = {'unit': 'week', 'n': 1}
        evidence = []
        for address, s in steady[:8]:
            per_week = len(s['items']) / DIGEST_WEEKS
            evidence.append(f"{s['name']} <{address}>: {len(s['items'])} mails in {DIGEST_WEEKS} weeks (about {per_week:.1f} a week), "
                            f"{s['unread']} still unread; latest: " + ' | '.join(f'"{t[:80]}" (event {i})' for _, t, i in s['items'][-2:]))
        if len(steady) > 8:
            evidence.append(f'and {len(steady) - 8} more senders like these')
        out.append({'key': 'pattern:mail:' + group, 'kind': 'mail', 'rule': rule,
                    'anchor': recurring.anchor_for(rule, today + dt.timedelta(days=1), weekday=DIGEST_DAY), 'at': DIGEST_AT,
                    'count': sum(len(s['items']) for _, s in steady), 'name': 'Promotions' if group == 'promo' else 'Newsletters',
                    'titles': [], 'evidence': evidence, 'why': {'kind': 'mail', 'n': len(steady)}})
    return out


def slack(db, today, tz, owner_ids=()):
    """Busy Slack channels: SLACK_WEEK or more messages by others in at least MIN_TIMES of the last four weeks, where the
    owner writes little (at most OWN_SHARE). Direct messages are conversations: never."""
    since = (today - dt.timedelta(weeks=4)).isoformat()
    owner_ids = {str(i) for i in owner_ids or ()}
    channels = {}
    for r in db.execute("SELECT id,occurred_at,body,metadata FROM events WHERE kind='slack.message' AND deleted=0 AND occurred_at>=? "
                        'ORDER BY occurred_at', (since,)):
        m = _meta(r['metadata'])
        channel = str(m.get('channel_id') or '')
        moment = _local(r['occurred_at'], tz)
        if not channel or channel.startswith('D') or not moment:
            continue
        c = channels.setdefault(channel, {'name': str(m.get('channel_name') or channel)[:60], 'weeks': Counter(), 'own': 0, 'all': 0, 'latest': []})
        c['all'] += 1
        if str(m.get('user_id') or '') in owner_ids or m.get('from_me') is True:
            c['own'] += 1
            continue
        c['weeks'][moment.isocalendar()[:2]] += 1
        c['latest'] = (c['latest'] + [(moment, r['body'], r['id'])])[-EVIDENCE:]
    out = []
    for channel, c in channels.items():
        busy = [w for w, n in c['weeks'].items() if n >= SLACK_WEEK]
        if len(busy) < MIN_TIMES or c['own'] > OWN_SHARE * c['all'] or not c['latest'] or (today - c['latest'][-1][0].date()).days > 7:
            continue
        rule = {'unit': 'week', 'n': 1}
        per_week = round(sum(c['weeks'].values()) / 4)
        out.append({'key': 'pattern:slack:' + channel, 'kind': 'slack', 'rule': rule,
                    'anchor': recurring.anchor_for(rule, today + dt.timedelta(days=1), weekday=DIGEST_DAY), 'at': DIGEST_AT,
                    'count': sum(c['weeks'].values()), 'name': '#' + c['name'].lstrip('#'), 'titles': [],
                    'evidence': [f"Slack channel #{c['name'].lstrip('#')} (channel_id {channel}): about {per_week} messages a week by others, "
                                 f"{c['own']} by the owner in four weeks. Latest:"] + [_line(m, b) + f' (event {i})' for m, b, i in c['latest']],
                    'why': {'kind': 'slack', 'n': per_week}})
    return out


def find(db, today, tz, owner_ids=()):
    """Every pattern that holds now, asked before or not."""
    return (asks(db, today, tz) + forward(db, today, tz) + sent(db, today, tz) + reply(db, today, tz) + slack(db, today, tz, owner_ids)
            + mail(db, today, tz))


def candidates(db, today, tz, owner_ids=(), skip=()):
    """Every new candidate, not in skip (origins and offer keys asked before), strongest first: by kind (KINDS), then by
    how often. A candidate whose to-do titles a recurring to-do series or offer already has is recurring.py's."""
    taken = {r[0] for r in db.execute('SELECT key FROM recurring_offers')} | set(skip)
    running = {recurring.title_key(r[0]) for r in db.execute('SELECT text FROM recurring_series WHERE stopped_at IS NULL')}
    out = [c for c in find(db, today, tz, owner_ids)
           if c['key'] not in taken and not any(t in running or 'title:' + t in taken for t in c['titles'])]
    return sorted(out, key=lambda c: (KINDS.index(c['kind']), -c['count']))
