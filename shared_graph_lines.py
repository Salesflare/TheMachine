"""A shared record's Timeline under Team (shared_graph.py): one line per real event, however many teammates had it.

The same email reaches several teammates' mailboxes, and each Machine writes its own line about it, in its owner's
language and its own words. A teammate's Machine sends each review line with `k`, a hash of the message's own id keyed
with the Fleet's graph key (only teammates' Machines can match it; the Network can't), and `lang`, the language it was
written in. The viewer's Machine folds lines that are the same event into one: the same `k`, or, from a Machine that
sends no `k` yet, lines from different teammates within minutes of each other on the same record (the same message
arrives everywhere at once; one teammate's own lines are each a fact already). The line it shows is the one in the
viewer's language, then the one that says who did what (it names someone on the record or in the team), then the
fullest, and it says every teammate it came from: "via Sam, Kim and Lee"."""
import datetime as dt
import re

import graph
import locale_prefs

WINDOW = dt.timedelta(minutes=3)  # one message, as several teammates' mailboxes have it
HEX = re.compile(r'[a-f0-9]{32}')


def unique_lines(found):
    """Timeline lines with each fact once, the newest kept (found: newest first)."""
    seen, out = set(), []
    for x in found:
        key = ' '.join(str(x.get('line') or '').split()).casefold()
        if key not in seen:
            seen.add(key)
            out.append(x)
    return out


def marks(k, reviewed):
    """What a line this Machine sends says beside its text: k, the message's Fleet-keyed hash, and for a review's
    line the language it was written in (the review writes in the owner's language)."""
    return {**({'k': k} if k else {}), **({'lang': locale_prefs.language()} if reviewed else {})}


def cleaned(x):
    """A teammate's line's k and lang, only in their fixed form."""
    return {**({'k': x['k']} if HEX.fullmatch(str(x.get('k'))) else {}),
            **({'lang': locale_prefs.code(x['lang'])} if locale_prefs.code(x.get('lang')) else {})}


def event_key(kind, metadata, at):
    """What makes a message the same one in every teammate's copy, or None: an email's Message-ID; a chat message's
    channel and time stamp; a conversation in a shared tool (Intercom, the CRM, GitHub, a document's comment) and when
    this part of it happened. Never a mailbox's own thread id (each mailbox has its own)."""
    m = metadata or {}
    mid = str(m.get('message-id') or '').strip().strip('<>').strip().lower()
    if mid:
        return 'mail|' + mid
    if kind == 'slack.message' and m.get('channel_id') and m.get('message_ts'):
        return f"slack|{m['channel_id']}|{m['message_ts']}"
    key, exact = graph.thread_key(kind, m)
    if key and exact and kind != 'gmail.message':
        return f'{key}|{at}'
    return None


def _when(at):
    try:
        moment = dt.datetime.fromisoformat(str(at or ''))
    except ValueError:
        return None
    return moment if moment.tzinfo else moment.replace(tzinfo=dt.timezone.utc)


def _same(group, line):
    """Whether a line from a teammate is the event this group is about."""
    if line.get('k') and line['k'] in group['keys']:
        return True
    if line['member'] in group['members'] or (line.get('k') and group['keys']):
        return False  # one teammate's lines are each their own fact; two message ids, two messages
    a, b = group['when'], _when(line.get('at'))
    return a is not None and b is not None and abs(a - b) <= WINDOW


def _rank(line, lang, names):
    """Which line of an event to show: the viewer's language (a line that doesn't say its language may be), then one
    that says who did what (it names a teammate or the record's own person), then the fullest."""
    words = str(line.get('line') or '').split()
    said = line.get('lang')
    tongue = 2 if said == lang else 1 if not said else 0
    named = any(w.strip('.,:;!?()"\'').casefold() in names for w in words)
    return tongue, named, min(len(words), 16), str(line.get('at') or '')


def merge(lines, lang, names=()):
    """lines: [{at, line, member, who, score, k?, lang?, tag?}] from every teammate, any order. Returns the Timeline
    lines, newest first: [{at, line, via: [first names, the closest teammate first], tag?}], each event once. lang:
    the viewer's (None: the owner's UI language now)."""
    lang = lang or locale_prefs.language()
    names ={str(n).casefold() for n in names if n}
    groups = []
    for x in sorted(lines, key=lambda x: str(x.get('at') or ''), reverse=True):
        group = next((g for g in groups if _same(g, x)), None)
        if group is None:
            group = {'when': _when(x.get('at')), 'keys': set(), 'members': set(), 'lines': []}
            groups.append(group)
        group['lines'].append(x)
        group['members'].add(x['member'])
        if x.get('k'):
            group['keys'].add(x['k'])
    out, by_text = [], {}
    for g in groups:
        best = max(g['lines'], key=lambda x: _rank(x, lang, names))
        who = [x['who'] for x in sorted(g['lines'], key=lambda x: -(x.get('score') or 0))]
        text = ' '.join(str(best['line']).split()).casefold()
        if text in by_text:  # the same words on another event: a thread's line on each of its messages, once
            kept = by_text[text]
            kept['via'] += [w for w in who if w not in kept['via']]
            continue
        line = {'at': best.get('at'), 'line': best['line'], 'via': list(dict.fromkeys(who)), **({'tag': best['tag']} if best.get('tag') else {})}
        by_text[text] = line
        out.append(line)
    return out
