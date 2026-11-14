"""The Fleet's brief, by plain code from cleaned facts (fleet.py): assemble_brief puts teammates' brief facts together
into "What the Fleet saw", overlap finds who is on separate threads with the same people at a company, and
brief_items and brief_text turn the view into a few ranked lines (settled: overlaps Not needed settled). Nothing here
reaches a model, the network or the database; fleet.py imports these names and the Fleet calls them."""
from __future__ import annotations

import collections
import datetime as dt
import re
import urllib.parse

import locale_prefs
from i18n import t


def overlap(threads):
    """{name: [thread]} of one company (each thread: hashes of its messages, `marks`, and of the people there on it)
    -> (names, threads): who is on a separate thread with the same people as another of you, and those threads (their
    marks). Separate: neither of the two is on the other's thread (no mark in common with any of their threads)."""
    who, found = [], []
    names = list(threads)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            seen_a = {m for t in threads[a] for m in t['marks']}
            seen_b = {m for t in threads[b] for m in t['marks']}
            for ta in threads[a]:
                for tb in threads[b]:
                    if set(ta['people']) & set(tb['people']) and not set(ta['marks']) & seen_b and not set(tb['marks']) & seen_a:
                        who += [n for n in (a, b) if n not in who]
                        found += [sorted(t['marks']) for t in (ta, tb) if sorted(t['marks']) not in found]
    return who, found


def assemble_brief(own, answers, claimed=(), members=None):
    """"What the Fleet saw", by plain code from cleaned facts: this Machine's own (as "You") and each teammate's that
    answered [(name, facts)]. Only what involves the team; nothing here reaches a model. `members` names the hashes of
    Fleet members' addresses ("You" for the owner's own).
    - quiet: companies that went quiet, that nobody was in touch with in the period, and that two or more of you knew
      or that are a customer;
    - several: companies where two or more of you each took part in a separate thread with the same people there
      (overlap): a real chance of talking past each other. One thread several of you are on, different people at
      the company, and contact one of you didn't take part in (mail that only came in, a support conversation a
      teammate handled) are not that;
    - unanswered: inbound emails the review said need something that nobody answered or claimed, and only when they
      involve the team: sent to two or more of you, to a shared address of the team, from a company another of you
      is in touch with, or from a customer. Mail only you got from someone only you
      know is for Suggestions, not here;
    - meetings: the same meeting on several calendars, or several of you meeting one company."""
    everyone = [('You', own)] + list(answers)
    members = members or {}
    orgs, touched, talks = {}, {}, {}

    def named(domain, org):  # a real company name wins over a bare domain, whoever has it
        if orgs.get(domain, domain) == domain:
            orgs[domain] = org
    for name, facts in everyone:
        for t in facts['touched']:
            named(t['domain'], t['org'])
            entry = touched.setdefault(t['domain'], {'who': {}, 'last': '', 'threads': {}, 'active': {}})
            entry['who'][name] = entry['who'].get(name, 0) + t['count']
            entry['last'] = max(entry['last'], t['last'])
            if t.get('active') and t.get('threads'):
                entry['threads'][name] = t['threads']
                entry['active'][name] = t['active']
            talks.setdefault(t['domain'], set()).add(name)
        for m in facts['meetings']:
            talks.setdefault(m['domain'], set()).add(name)
    quiet = {}
    for name, facts in everyone:
        for q in facts['quiet']:
            if q['domain'] in touched:
                continue
            named(q['domain'], q['org'])
            entry = quiet.setdefault(q['domain'], {'who': [], 'last': '', 'known': ''})
            if name not in entry['who']:
                entry['who'].append(name)
            entry['last'] = max(entry['last'], q['last'])
            entry['known'] = entry['known'] or q.get('known') or ''
    replied = {k for _, facts in everyone for k in facts['replied']} | set(claimed)
    emails = {}
    for name, facts in everyone:
        for u in facts['unanswered']:
            if u['key'] in replied:
                continue
            named(u['domain'], u['org'])
            entry = emails.setdefault(u['key'], {'domain': u['domain'], 'at': u['at'], 'who': [], 'shared': set(), 'known': ''})
            for who in [name] + [members[h] for h in u.get('team') or () if h in members]:
                if who not in entry['who']:
                    entry['who'].append(who)
            entry['shared'] |= set(u.get('shared') or ())
            entry['known'] = entry['known'] or u.get('known') or ''
            entry['at'] = min(entry['at'], u['at'])
    open_ = {}
    for key, e in emails.items():
        also = talks.get(e['domain'], set()) - set(e['who'])
        if len(e['who']) < 2 and not e['shared'] and not also and not e['known']:
            continue  # only you got it, from someone only you know: that's for Suggestions
        entry = open_.setdefault(e['domain'], {'keys': set(), 'who': [], 'since': e['at'], 'shared': set(), 'also': set(), 'known': ''})
        entry['keys'].add(key)
        entry['since'] = min(entry['since'], e['at'])
        entry['who'] += [w for w in e['who'] if w not in entry['who']]
        entry['shared'] |= e['shared']
        entry['also'] |= also
        entry['known'] = entry['known'] or e['known']
    by_key, by_domain = {}, {}
    for name, facts in everyone:
        for m in facts['meetings']:
            named(m['domain'], m['org'])
            same = by_key.setdefault(m['key'], {'domain': m['domain'], 'day': m['day'], 'who': []})
            if name not in same['who']:
                same['who'].append(name)
            by_domain.setdefault(m['domain'], {}).setdefault(name, set()).add(m['day'])
    meetings = [{'org': orgs[s['domain']], 'domain': s['domain'], 'day': s['day'], 'who': s['who'], 'same': True}
                for s in by_key.values() if len(s['who']) > 1]
    covered = {m['domain'] for m in meetings}
    meetings += [{'org': orgs[d], 'domain': d, 'day': min(min(days) for days in who.values()), 'who': sorted(who), 'same': False}
                 for d, who in by_domain.items() if len(who) > 1 and d not in covered]
    return {'quiet': [{'org': orgs[d], 'domain': d, 'last': e['last'], 'who': e['who'], **({'known': e['known']} if e['known'] else {})}
                      for d, e in sorted(quiet.items(), key=lambda kv: kv[1]['last']) if len(e['who']) > 1 or e['known']][:10],
            'several': [{'org': orgs[d], 'domain': d, 'last': max(e['active'][n] for n in who), 'who': [{'name': n, 'count': e['who'][n]} for n in who],
                         'threads': threads}
                        for d, e in sorted(touched.items(), key=lambda kv: (-len(kv[1]['who']), -sum(kv[1]['who'].values())))
                        for who, threads in [overlap(e['threads'])] if who][:10],
            'unanswered': [{'org': orgs[d], 'domain': d, 'count': len(e['keys']), 'since': e['since'], 'who': e['who'],
                            **({'shared': sorted(e['shared'])} if e['shared'] else {}),
                            **({'also': sorted(e['also'] - set(e['who']))} if e['also'] - set(e['who']) else {}),
                            **({'known': e['known']} if e['known'] else {})}
                           for d, e in sorted(open_.items(), key=lambda kv: kv[1]['since'])][:10],
            'meetings': sorted(meetings, key=lambda m: m['day'])[:10],
            'from': [name for name, _ in answers]}


BRIEF_SHOWN = 5  # items a brief shows before "Show more"
QUIET_MIN_DAYS = 14  # the Graph's own floor for gone quiet (graph.build): in touch more recently than this isn't quiet


def _brief_date(value):
    try:
        return dt.date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def _on_day(value, today):
    """A day as people say it: today, tomorrow, yesterday, Thu, Oct 12."""
    d = _brief_date(value)
    if not d:
        return ''
    gap = (d - today).days
    if gap == 0:
        return t('today')
    if gap == 1:
        return t('tomorrow')
    if gap == -1:
        return t('yesterday')
    if -6 <= gap <= 6:
        return locale_prefs.weekday_name(d)
    return locale_prefs.day_text(d, weekday=False)


def _waited(value, today):
    d = _brief_date(value)
    days = (today - d).days if d else 0
    return days, (t('since yesterday') if days == 1 else t('{} days', days) if days < 7 else t('since {}', locale_prefs.day_text(d, weekday=False)))


def _plain_name(label):
    """A teammate's label as a name: without "(their@address)" or any address in it."""
    text = re.sub(r'\([^)]*\)|<[^>]*>|\S+@\S+', ' ', str(label or ''))
    return ' '.join(text.split()) or 'A teammate'


def _first_names(view):
    """Teammates by first name when that's unambiguous in this brief ("Priya" for Priya Okonedo), never an address."""
    everyone = {w if isinstance(w, str) else w.get('name') for k in ('unanswered', 'several', 'meetings', 'quiet') for x in view.get(k) or []
                for w in (x.get('who') or []) + (x.get('also') or [])} | set(view.get('from') or []) | set(view.get('missing') or [])
    everyone = {str(n) for n in everyone if n and n != 'You'}
    first = collections.Counter(_plain_name(n).split()[0] for n in everyone)
    return {n: _plain_name(n).split()[0] if first[_plain_name(n).split()[0]] == 1 else _plain_name(n) for n in everyone}


def _people(who, short=None, after=False):
    """Names in a row, you first: 'you, Pat and Kim'. after: they follow a word ("sent to you"), which some languages
    say differently ("jou", "dich")."""
    who = sorted(who, key=lambda w: w != 'You')  # you first
    names = [(t('you (after a word)') if after else t('you')) if w == 'You' else (short or {}).get(w, w) for w in who]
    return names[0] if len(names) == 1 else ', '.join(names[:-1]) + t(' and {}', names[-1]) if names else ''


def company(x):
    """A company as people name it: the graph's name, else the domain's own name ("scribbl.co" → Scribbl)."""
    org, domain = str(x.get('org') or ''), str(x.get('domain') or '')
    if org and org.lower() != domain.lower():
        return org
    labels = domain.lower().split('.')
    name = labels[-3] if len(labels) >= 3 and labels[-2] in ('co', 'com', 'org', 'net', 'ac', 'gov') else labels[0] if len(labels) < 3 else labels[-2]
    return name[:1].upper() + name[1:] if name else domain


def _cap(text):
    return text[:1].upper() + text[1:]


def gmail_search(domain):
    return 'https://mail.google.com/mail/#search/' + urllib.parse.quote(f"from:{domain} in:inbox")


KNOWN_WHY = {'customer': 'a customer'}  # read through t()


def _team_why(x, people):
    """Why a waiting email is the team's: who got it, a shared address, a teammate in touch, a customer. '' when none."""
    who, also = x.get('who') or [], x.get('also') or []
    why = []
    if len(who) > 1 or (who and 'You' not in who):
        why.append(t('sent to {}', people(who, True)))
    if x.get('shared'):
        why.append(t('to {} (a shared address)', ', '.join(f"{s}@" for s in x['shared'])))
    if also:
        why.append(t('{} also talks to them', people(also)) if len(also) == 1 and also[0] != 'You' else t('{} also talk to them', people(also)))
    if x.get('known') in KNOWN_WHY:
        why.append(t(KNOWN_WHY[x['known']]))
    team = len(who) > 1 or x.get('shared') or also or x.get('known') in KNOWN_WHY
    return ', '.join(why) if team else ''


def settled(learned, x):
    """Whether Not needed already settled this overlap (Fleet.hide_brief_item): the same company, the same people of
    the team, and every thread of it one the owner said wasn't needed (a mark in common: a reply carries the Message-ID
    it answers). A new thread brings it back."""
    seen = learned.get('several:' + str(x.get('domain')))
    if not seen or set(seen.get('who') or ()) != {w['name'] for w in x.get('who') or []}:
        return False
    marks = set(seen.get('marks') or ())
    return all(set(t) & marks for t in x.get('threads') or ())


def brief_items(view, today=None, hidden=(), opener=None, learned=None, limit=12):
    """The brief as a few ranked lines worth reading: who is waiting on the team and for how long, where several of you
    are on the same company or meeting, and companies that went quiet that a teammate knows. Each item has a stable key
    (for Not needed), a title, why it matters and, where the Fleet can help, a question to ask it. `opener(domain)` links
    the owner's own waiting mail (a Gmail search by default). `learned`: overlaps Not needed settled for good
    (Fleet.brief_learned). Plain code."""
    import timeutil
    opener = opener or gmail_search
    today = today or timeutil.clock().date()
    short = _first_names(view)
    people = lambda who, after=False: _people(who, short, after)
    items = []
    for x in view.get('unanswered') or []:
        days, waited = _waited(x.get('since'), today)
        who, also = x.get('who') or [], x.get('also') or []
        team = [w for w in who if w != 'You']
        if days < 1 or (not team and days < 2):  # today's mail isn't waiting yet; your own needs a couple of days
            continue
        several = len(who) > 1
        why = _team_why(x, people)
        if not why:  # only you got it, from someone only you know (a brief from before 2026-10-21): that's for Suggestions
            continue
        count = x.get('count') or 1
        items.append({'key': 'unanswered:' + x['domain'], 'kind': 'waiting', 'score': 100 + min(days, 14) * 5 + (20 if several else 0),
                      'title': t('{} is waiting for a reply', company(x)) + (t(' ({} emails)', count) if count > 1 else ''),
                      'why': f"{waited}, {why}", 'ask': t('Who is answering {}?', company(x)),
                      'open': opener(x['domain']) if 'You' in who else '', **_raw(x, x.get('since'), who + [w for w in also if w not in who], short),
                      'to': [short.get(w, w) for w in team], 'to_me': 'You' in who})
    for x in view.get('meetings') or []:
        d = _brief_date(x.get('day'))
        soon = d is not None and 0 <= (d - today).days <= 3
        items.append({'key': 'meeting:' + x['domain'] + ':' + str(x.get('day')), 'kind': 'meeting', 'score': (80 if soon else 50) + len(x['who']),
                      'title': t('{} meet {} {} (a meeting in the brief)', _cap(people(x['who'])), company(x), _on_day(x.get('day'), today)).rstrip(),
                      'why': t('the same meeting, so agree who leads') if x.get('same') else t('separate meetings, worth lining up'),
                      'ask': t('Who leads with {}?', company(x)), **_raw(x, x.get('day'), x.get('who') or [], short)})
    for x in view.get('several') or []:
        who = [w['name'] for w in x.get('who') or []]
        if settled(learned or {}, x):
            continue
        items.append({'key': 'several:' + x['domain'], 'kind': 'overlap', 'score': 60 + len(who),
                      'title': t('{} are all in touch with {}', _cap(people(who)), company(x)) if len(who) > 2 else t('{} are both in touch with {}', _cap(people(who)), company(x)),
                      'why': t('last contact {}, so keep it to one thread', _on_day(x.get('last'), today)), 'ask': t('Who leads with {}?', company(x)),
                      **_raw(x, x.get('last'), who, short)})
    for x in view.get('quiet') or []:
        who = x.get('who') or []
        if len(who) < 2 and not x.get('known'):  # one of you, a company the team doesn't know (a brief from before 2026-10-21)
            continue
        last = _brief_date(x.get('last'))
        if not last or (today - last).days < QUIET_MIN_DAYS:  # a person gone quiet, but someone there wrote lately: not quiet
            continue
        why = [t('known to {}', people(who, True))] if len(who) > 1 else []
        why += [t(KNOWN_WHY[x['known']])] if x.get('known') in KNOWN_WHY else []
        items.append({'key': 'quiet:' + x['domain'], 'kind': 'quiet', 'score': 40 + (10 if len(who) > 1 else 0),
                      'title': t('{} went quiet', company(x)),
                      'why': ', '.join([t('last contact {}', _on_day(x.get('last'), today))] + why),
                      'ask': t('Anyone in touch with {} lately?', company(x)), **_raw(x, x.get('last'), who, short)})
    hidden = set(hidden)
    items = [i for i in items if i['key'] not in hidden]
    items.sort(key=lambda i: -i['score'])
    return items[:limit] if limit else items


def _raw(x, at, who, short):
    """What a brief line's to-do needs besides its words (fleet_brief_todos.py): the company, the day it hangs on (the
    first waiting email, the meeting, the last contact) and the people of the team on it ('You' for the owner), each
    with how the line names them. Only what the brief view already holds."""
    return {'org': company(x), 'domain': str(x.get('domain') or ''), 'at': str(at or '')[:10], 'known': x.get('known') or '',
            'team': [{'label': w, 'name': (short or {}).get(w, w)} for w in who if w and w != 'You'], 'mine': 'You' in who}


def brief_text(view, today=None, hidden=(), learned=None):
    """The brief as plain lines, for the Telegram message (To-dos carry brief_items as to-dos: fleet_brief_todos.py)."""
    head = (t('Your Fleet this week') if view.get('every') == 'week' else t('Your Fleet today')) + (f" · {view['fleet_name']}" if view.get('fleet_name') else '')
    items = brief_items(view, today, hidden, learned=learned)
    lines = [head] + [f"• {i['title']}. {_cap(i['why'])}." for i in items[:BRIEF_SHOWN]]
    if len(items) > BRIEF_SHOWN:
        lines.append(t('…and {} more in To-dos.', len(items) - BRIEF_SHOWN))
    if not items:
        lines.append(t('Nothing that needs the team.'))
    told = view.get('from') or []
    lines += ['', t('From {}.', _people(['You'] + told, _first_names(view), True)) if told else t('Only from your own Machine so far.')]
    if view.get('missing'):
        lines.append(t('Still to answer: {}.', _people(view['missing'], _first_names(view))))
    return '\n'.join(lines)
