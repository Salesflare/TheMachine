"""The weekly recap in the service (refactor PR 26): the recap message with its Graph and sharing lines and its
buttons, the step that makes one and pushes it, and the owner's choices on it. Moved out of assistant.App as is. A
mixin of assistant.App (APP_MIXINS)."""
import collections
import datetime as dt
import json
import re
import secrets
import sqlite3
import subprocess
import threading

import graph
import i18n
import locale_prefs
from machine.cards import looks_done, plain, waits_on_others
from machine.config import LOG
from machine.delivery.push import app_wake, push_node, quick_web
from machine.delivery.telegram import DeliveryNotSent, telegram_request
from machine.model_usage import telegram_account, telegram_on
from machine.sources.android import android_app_name
from machine.sources.calendar import calendar_keys, calendar_owned
from machine import names as display_names
from machine.sources.connectors import UNNAMED
from machine.sources.exclusions import default_exclusions
from machine.app.recap_settings import recap_settings
from machine.store.first_look import FirstLookStore
from machine.store.profile import recap_day
from machine.text import encoded
import notify
import security_levels
import still_needed
import team_learnings
from timeutil import local_tz, now


def recap_escape(text):
    """Owner data in the recap's Telegram markdown: shown as written, never as formatting or a link."""
    return re.sub(r'([\\`*_\[\]~])', r'\\\1', str(text))


def recap_clip(text, limit=70):
    text = ' '.join(str(text or '').split())
    return text if len(text) <= limit else text[:limit - 1].rstrip() + '…'


def recap_noise(db, since):
    """Automated sources that were busy this week and led to no card, each with the `exclude` rule that would filter it:
    {(account, where): {'n', 'rule'}}. Only automated sources are candidates, never people's own conversations: a group chat
    the owner writes in this week, or a small circle of people, is someone's own chat (friends, family), not noise."""
    used = set()
    for (ids,) in db.execute('SELECT event_ids FROM suggestions'):
        used |= set(json.loads(ids))
    noise, circle = {}, collections.defaultdict(lambda: {'mine': 0, 'people': set()})
    for i, account, kind, m in db.execute('SELECT id,account_id,kind,metadata FROM events WHERE ingested_at>=? AND history=0', (since,)):
        m = json.loads(m)
        if (kind == 'whatsapp.message' and str(m.get('chat_id', '')).endswith('@g.us')) or (kind == 'telegram.message' and m.get('chat_kind') == 'group'):
            chat = circle[(account, m['chat_id'])]  # who takes part, from every message in it (cards or not)
            if m.get('from_me'):
                chat['mine'] += 1
            elif m.get('sender_id') or m.get('from'):
                chat['people'].add(m.get('sender_id') or m.get('from'))
        if i in used:
            continue
        sender = re.sub(r'.*<|>.*', '', str(m.get('from') or '')).strip()
        if kind == 'slack.message' and m.get('channel_name') and not str(m['channel_name']).startswith('DM '):
            where, rule = '#' + m['channel_name'], {'channels': [m['channel_name']]}
        elif kind == 'whatsapp.message' and str(m.get('chat_id', '')).endswith('@g.us'):
            where, rule = m.get('chat_name') or 'WhatsApp group', {'chats': [m['chat_id']]}
        elif kind == 'telegram.message' and m.get('chat_kind') == 'group' and m.get('chat_id'):
            where, rule = m.get('chat_name') or 'Telegram group', {'chats': [m['chat_id']]}
        elif kind == 'android.notification' and m.get('package_name'):
            app = str(m.get('app_name') or android_app_name(m['package_name']))
            app = app.rsplit('.', 1)[-1] if re.fullmatch(r'[\w]+(?:\.[\w]+)+', app) else app  # com.Slack → Slack
            where, rule = app[:1].upper() + app[1:] + ' notifications', {'packages': [m['package_name']]}
        elif kind in ('gmail.message', 'salesflare.email') and sender and re.search(r'(?i)no-?reply|notification|alert|digest|news|mailer|updates?@', sender):
            where, rule = sender, {'senders': [sender.lower()]}
        else:
            continue
        noise.setdefault((account, where), {'n': 0, 'rule': rule})['n'] += 1
    own = lambda account, rule: any(c['mine'] or len(c['people']) <= RECAP_CIRCLE for c in [circle[(account, rule['chats'][0])]]) if 'chats' in rule else False
    return {k: v for k, v in noise.items() if not own(k[0], v['rule'])}


def recap_named(node):
    """Someone known by a name of their own: not an address or a domain, and not their organization's own name
    (a company's desk writing as the company, like a support team signing with the product's name)."""
    name = ' '.join(str(node.get('name') or '').split())
    if not name or '@' in name or re.search(r'\S\.[a-z]{2,}\b', name, re.I):
        return False
    org = str(node.get('org') or '').removeprefix('org:').casefold()
    labels = [label for label in org.split('.')[:-1] if label]
    return not (len(name.split()) == 1 and any(name.casefold() in label for label in labels))


def recap_graph_lines(store, since=None):
    """What's alive this week: projects heating up or cooling, who is new (by name), who has gone quiet (with what they
    are to the owner, or their organization's role: "a customer went quiet"), and roles waiting for the owner's ✓."""
    try:
        with store.connect() as db:
            view = graph.overview(db, 3)
            orgs = {r['id']: (r['name'], json.loads(r['info']).get('role')) for r in db.execute("SELECT id,name,info FROM graph_nodes WHERE kind='org'")}
            made = [(r['name'], r['made']) for r in db.execute("SELECT name,json_extract(info,'$.created_at') made FROM graph_nodes WHERE kind='project' "
                                                                "AND json_extract(info,'$.closed_at') IS NULL ORDER BY strength DESC")]
    except sqlite3.Error:
        return []
    out, t = [], i18n.t
    for state, line in (('heating up', 'Busier lately: {}'), ('active', 'Steady: {}'), ('cooling', 'Quieter lately: {}')):
        names = [recap_escape(p['name']) for p in view['projects'] if p['state'] == state][:3]
        if names:
            out.append('• ' + t(line, ', '.join(names)))

    def who(p):
        org, org_role = orgs.get(p.get('org'), (None, None))
        what = p.get('role') or (t('at {}, {}', org, org_role) if org_role else None)
        gap = round(p['usual_gap_days'])
        return recap_escape(p['name'] + ' (' + (what + ', ' if what else '') + (t('usually daily') if gap <= 1 else t('usually every {} days', gap)) + ')')
    named = [p for p in view['new'] if recap_named(p)]
    unnamed = sum(1 for p in view['new'] if '@' in str(p.get('name') or ''))  # known only by their address so far
    if named:
        more = t(', and {} more known only by address', unnamed) if unnamed else ''
        out.append('• ' + t('New people: {}', ', '.join(recap_escape(p['name']) for p in named[:4])) + more)
    # New projects, once the graph is older than this week (on its first week every project is new).
    if since and made and all(m for _, m in made) and min(m for _, m in made) < since:
        fresh = [recap_escape(n) for n, m in made if m >= since][:3]
        if fresh:
            out.append('• ' + t('New projects: {}', ', '.join(fresh)))
    if view['quiet']:
        out.append('• ' + t('Gone quiet: {}', ', '.join(who(p) for p in view['quiet'])))
    return out


def recap_share_lines(store, config):
    """The Shared Graph's line in the weekly report: what went to each Work Fleet and how much was held back, with a link
    to look over the held-back ones (shared_graph.py)."""
    out = []
    with store.connect() as db:
        rows = db.execute("SELECT key,value FROM fleet_meta WHERE key LIKE 'graph_week:%'").fetchall() if db.execute(
            "SELECT 1 FROM sqlite_master WHERE name='fleet_meta'").fetchone() else []
        directory = db.execute("SELECT value FROM fleet_meta WHERE key='directory'").fetchone() if rows else None
    names = {f.get('id'): f.get('name') for f in (json.loads(directory['value']) or {}).get('fleets', [])} if directory else {}
    host = str(config.get('dashboard_host') or '')
    for row in rows:
        week, fleet_id = json.loads(row['value']) or {}, row['key'].split(':', 1)[1]
        if fleet_id not in names:
            continue
        held = week.get('held') or 0
        line = '• ' + i18n.t('Shared {} threads with {} this week, {} held back.', week.get('threads', 0), names[fleet_id] or i18n.t('your team'), held)
        if host:
            line += ' [' + i18n.t("What's shared") + f"]({'https://' + host + config.get('dashboard_path', '/') + '#shared=' + fleet_id})"
        out.append(line)
    return out


RECAP_CIRCLE = 8  # a group chat with this many others or fewer is a circle of people, not a broadcast


RECAP_CHOICES = {'noise': ('filter', 'keep', 'undo'), 'snoozed': ('drop', 'now', 'keep'), still_needed.KIND: ('drop', 'keep')}


RECAP_DONE = {'filtered': 'No longer checked', 'kept': 'Kept', 'dropped': 'Not needed', 'started': 'Started'}


# Recaps sent before each choice had its own message: their buttons sit under the recap, numbered like its lines.
RECAP_DONE_NUMBERED = {**RECAP_DONE, 'filtered': 'Filtered'}


def recap_buttons(items, numbered=False):
    """One row per line still open: Stop reviewing / Keep reviewing for a busy source, Not needed / Do it / Keep for a
    card snoozed again and again; a filtered source keeps Undo. Each choice is its own message, so a label needs no
    number; numbered is for a recap sent before that, whose buttons sit under the whole recap."""
    rows = []
    for item in items:
        value = f"assistant:recap:{item['id']}:"
        label = (lambda text: f"{i18n.t(text)} {item['n']}") if numbered else i18n.t
        if item['status'] == 'open':
            choices = ([('Filter', 'filter'), ('Keep', 'keep')] if numbered else [('Stop checking', 'filter'), ('Keep checking', 'keep')]) \
                if item['kind'] == 'noise' else [('Not needed', 'drop'), ('Do it', 'now'), ('Keep', 'keep')]
            rows.append([{'text': label(text), 'value': value + choice} for text, choice in choices])
        elif item['status'] == 'filtered':
            rows.append([{'text': label('Undo'), 'value': value + 'undo'}])
    return rows


def recap_view(text, items):
    """A recap sent before each choice had its own message, as it stands now: each decided line says what was done,
    and only open lines keep their (numbered) buttons."""
    for item in items:
        if item['status'] in RECAP_DONE_NUMBERED:
            text = text.replace(item['line'], item['line'] + ' · **' + i18n.t(RECAP_DONE_NUMBERED[item['status']]) + '**', 1)
    return {'text': text, 'buttons': recap_buttons(items, numbered=True)}


def recap_choice_view(item):
    """One choice's own message as it stands now: its line, what was done once decided, and the buttons still open."""
    done = ' · **' + i18n.t(RECAP_DONE[item['status']]) + '**' if item['status'] in RECAP_DONE else ''
    return {'text': item['line'] + done, 'buttons': recap_buttons([item])}


def recap_presentation(buttons):
    """The same rows as Telegram presentation blocks for the message tool (send and edit)."""
    blocks = [{'type': 'buttons', 'buttons': [{'label': b['text'], 'action': {'type': 'callback', 'value': b['value']}} for b in row]} for row in buttons]
    return {'blocks': blocks or [{'type': 'buttons', 'buttons': []}]}


def recap_meetings(db, start, end, cards):
    """The week ahead's meetings worth a line: the owner's own (calendar_owned: on a shared calendar, only those they
    organize or are invited to), with other people, said yes or not answered, and either a one-off or one with a card on
    it (a weekly one-on-one is routine, unless something is prepared for it). A meeting on two calendars shows once."""
    seen, out = set(), []
    for r in db.execute("SELECT id,title,occurred_at,metadata FROM events WHERE kind='calendar.event' AND deleted=0 AND occurred_at>=? AND occurred_at<? "
                        'ORDER BY occurred_at,id LIMIT 300', (start, end)):
        m = json.loads(r['metadata'])
        if not calendar_owned(m):
            continue
        people = [x for x in m.get('attendees') or [] if isinstance(x, dict)]
        if m.get('access') == 'shared_read_only':  # 'self' there is the calendar's owner: the Machine's owner is by address
            mine = str(m.get('credential_account') or '').lower()
            is_me = lambda x: str(x.get('email') or '').lower() == mine
        else:
            is_me = lambda x: bool(x.get('self'))
        me = next((x for x in people if is_me(x)), {})
        card = cards.get(r['id'])
        if m.get('all_day') or me.get('responseStatus') == 'declined' or m.get('status') == 'cancelled':
            continue
        others = [x for x in people if not is_me(x)]
        if not others or (m.get('recurring_event_id') and not card):
            continue
        keys = calendar_keys(m, r['title'], r['occurred_at'], None)
        if keys & seen:
            continue
        seen |= keys
        out.append({'at': r['occurred_at'], 'title': r['title'], 'guests': len(others), 'card': card})
    return out


def weekly_recap_message(store, config, current=None):
    """Friday recap, made to act on: what needs the owner first (late promises, their own with a date), the week ahead,
    what changed and whether it works, and behind the scenes in one short line (no cost: the recap may go to anyone
    with a Machine). Then busy sources and cards snoozed again and again, each a choice of its own that changes only
    the owner's own filters or cards. Returns {'text', 'items'}: text is the recap message, and each item one choice
    with its own short message ('line', read without the recap) and buttons (not stored yet)."""
    current = current or dt.datetime.fromisoformat(now())
    tz = local_tz()
    since = (current - dt.timedelta(days=7)).isoformat()
    today = current.astimezone(tz).date()
    # The week ahead: tomorrow through the same weekday next week (a Friday recap: Saturday to Friday).
    tomorrow = today + dt.timedelta(days=1)
    start_ahead = dt.datetime.combine(tomorrow, dt.time(), tz).astimezone(dt.timezone.utc).isoformat()
    ahead = dt.datetime.combine(tomorrow + dt.timedelta(days=7), dt.time(), tz).astimezone(dt.timezone.utc).isoformat()
    in_week = lambda day: tomorrow.isoformat() <= str(day)[:10] < (tomorrow + dt.timedelta(days=7)).isoformat()
    root = 'https://' + config['dashboard_host'] + config.get('dashboard_path', '/') if config.get('dashboard_host') else ''
    link = lambda text, card: f'[{recap_escape(text)}]({root}#chat={card})' if root and card else recap_escape(text)
    names = {x['id']: display_names.account_name(x, config.get('accounts', []), UNNAMED.get(x.get('service'))) for x in config.get('accounts', [])}
    with store.connect() as db:
        batches = [json.loads(r[0]) for r in db.execute("SELECT items FROM analyses WHERE status='complete' AND finished_at>=?", (since,))]
        reviewed = sum(sum(1 for i in items if not i.get('deferred') and not i.get('excluded')) for items in batches)
        backlog = db.execute('SELECT count(*) FROM events WHERE analyzed_version<version').fetchone()[0]
        noise = recap_noise(db, since)
        open_cards = {r['id']: dict(r) for r in db.execute(
            "SELECT id,title,status,due,event_ids FROM suggestions WHERE status IN ('pending','accepted','instructions','prepared','snoozed')")}
        on_event = {}
        for card in open_cards.values():
            for e in json.loads(card['event_ids']):
                on_event.setdefault(e, card)
        meetings = recap_meetings(db, start_ahead, ahead, on_event)
        snoozed = [dict(r) for r in db.execute(
            "SELECT d.suggestion_id id,count(*) n,max(d.created_at) last FROM decisions d JOIN suggestions s ON s.id=d.suggestion_id WHERE d.choice='snooze' "
            "AND d.source IN ('telegram','dashboard') AND d.created_at>=? AND s.status IN ('snoozed','pending') GROUP BY d.suggestion_id HAVING n>=2 ORDER BY n DESC,last DESC",
            (since,))]
        # A source or card the owner said Keep to in an earlier recap isn't offered again (a card only until it is snoozed again).
        kept = [dict(r) for r in db.execute("SELECT kind,ref,data,decided_at FROM recap_items WHERE status='kept'")]
        changes = [dict(r) for r in db.execute('SELECT at,kind,text FROM rule_changes WHERE at>=? ORDER BY at', (since,))]
    kept_rules = [json.loads(k['data']).get('rule') for k in kept if k['kind'] == 'noise']
    kept_cards = {k['ref']: k['decided_at'] for k in kept if k['kind'] == 'snoozed'}
    start_local, end_local = dt.datetime.fromisoformat(since).astimezone(tz), current.astimezone(tz)
    span = locale_prefs.span_text(start_local, end_local)
    t = i18n.t  # the recap goes out now: in the owner's language
    lines = ['**' + t('Your week with The Machine') + f'** · {span}']

    # 1. What needs the owner: promises made to them that are late, then their own open ones with a date.
    promised = [p for p in store.promises(7) if p['state'] in ('open', 'card')]
    # A promise links to its own page on the dashboard, never to its card (the page links the card)
    said = lambda p: f"[{recap_escape(recap_clip(p['what']))}]({root}#promise/{p['id']})" if root else recap_escape(recap_clip(p['what']))
    late_to = [p for p in promised if p['direction'] == 'theirs' and ((p['due'] and p['due'] < today.isoformat()) or (not p['due'] and p['check_at'] <= current.isoformat()))]
    soon = (today + dt.timedelta(days=14)).isoformat()  # their own: late ones and those due in the next two weeks
    mine = sorted((p for p in promised if p['direction'] == 'mine' and p['due'] and p['due'] <= soon), key=lambda p: p['due'])
    needs = ['• ' + t('Waiting on {}: {}, ', recap_escape(p['who']), said(p))
             + (t('due {}', recap_day(p['due'])) if p['due'] else t('since {}', recap_day(p['made_at']))) for p in late_to[:4]]
    needs += ['• ' + t('Promised {}: {}, ', recap_escape(p['who']), said(p))
              + (t('was due {}', recap_day(p['due'])) if p['due'] < today.isoformat() else t('due {}', recap_day(p['due']))) for p in mine[:4]]
    more = max(0, len(late_to) - 4) + max(0, len(mine) - 4)
    if needs:
        lines += ['', '**' + t('Needs you') + '**', *needs] + (['• ' + t('{} more in Promises', more) + (' ' + t('on the [dashboard]({})', root) if root else '')] if more else [])

    # 2. The week ahead: meetings worth preparing, cards due and dates others promised.
    week = []
    for m in meetings[:5]:
        card = m['card']
        prep = (' · ' + link(t('prep ready') if card['status'] == 'prepared' else t('to-do'), card['id'])) if card else ''
        week.append((m['at'], f"• {recap_day(m['at'], True)} {recap_escape(recap_clip(m['title'], 60))}, {t('{} people', m['guests'])}{prep}"))
    listed = {m['card']['id'] for m in meetings[:5] if m['card']}
    for card in open_cards.values():
        if card['due'] and in_week(card['due']) and card['id'] not in listed:
            week.append((card['due'], f"• {recap_day(card['due'][:10])}: " + t('{} is due', link(recap_clip(card['title']), card['id']))))
    for p in promised:
        same = lambda q: q['direction'] == 'mine' and q['who'] == p['who'] and q['what'].lower() == p['what'].lower()
        if p['direction'] == 'theirs' and p['due'] and in_week(p['due']) and not any(map(same, mine)):  # today's are on time, late ones are under Needs you, a shared plan shows once
            week.append((p['due'], f"• {recap_day(p['due'])}: " + t("{} said they'd {}", recap_escape(p['who']), said(p))))
    if week:
        when = lambda v: str(v) if len(str(v)) <= 10 else dt.datetime.fromisoformat(str(v).replace('Z', '+00:00')).astimezone(tz).strftime('%Y-%m-%dT%H:%M')
        week.sort(key=lambda w: when(w[0]))
        lines += ['', '**' + t('Next week') + '**', *[w for _, w in week[:8]]]

    # 3. What changed: the hit rate in one line, what it learned and whether that works.
    q, before = store.quality(7, current.isoformat()), store.quality(7, since)
    changed = []
    if q['hit_rate'] is not None:
        was = before['hit_rate']
        trend = '' if was is None else t(', same as the week before') if was == q['hit_rate'] else t(', up from {}%', was) if q['hit_rate'] > was else t(', down from {}%', was)
        first = ' ' + t('Do it was right first time in {} of {}.', q['first_time'], q['do_it']) if q['do_it'] else ''
        changed.append('• ' + t('{}% of to-dos worth it ({} of {})', q['hit_rate'], q['worth_it'], q['worth_it'] + q['dismissed']) + f"{trend}.{first}")
    learned = store.behaviour(7)
    rules = sum(1 for c in changes if c['kind'] == 'draft_rule' and not c['text'].startswith('Removed'))
    voices = sum(1 for c in changes if c['kind'] == 'voice')
    guide = sum(1 for c in changes if c['kind'] == 'file' and c['text'] == 'PREPARATION.md edited')  # what behaviour() counts as a rule change
    filters = sum(1 for c in changes if c['kind'] == 'filter' and not c['text'].startswith('Removed'))
    bits = [b for n, b in ((rules, t('{} writing rules', rules)), (voices, t('{} updates to how you write', voices)),
                           (guide, t('{} edits to the drafting guide', guide)), (filters, t('{} new filters', filters))) if n]
    sent = learned['sent_as_written'] + learned['sent_edited']
    s = learned['since_rules']
    if bits:
        done = (s['as_written'] + s['edited']) if s else 0
        works = (' ' + t('Since then, {} of {} drafts went out as written', s['as_written'], done) + (' ' + t('({} of {} before).', learned['sent_as_written'] - s['as_written'], sent - done) if sent > done else '.')
                 if s and done else ' ' + t('No drafts sent since then yet.') if s else '')
        changed.append('• ' + t('Adjusted: {}.', ', '.join(bits)) + works)
    elif sent:
        changed.append('• ' + t('Drafts: {} of {} went out as written.', learned['sent_as_written'], sent))
    if changed:
        lines += ['', '**' + t('What changed') + '**', *changed]
    with store.connect() as db:
        share = team_learnings.waiting(db)
    if share:  # only a pointer: they go out from Learning, Shared, after the owner read them
        lines += ['', '**' + t('For The Machine team') + '**', '• ' + t('{} learnings to share, if you like: ', share)
                  + (f"[{t('read them')}]({root}#learning=shared)" if root else t('read them under Learning')) + '. ' + t('Nothing goes without your OK.')]
    alive = recap_graph_lines(store, since) + recap_share_lines(store, config)
    if alive:
        lines += ['', '**' + t('People and projects') + '**', *alive]

    # 4. Behind the scenes, in one short line: what was read, never what it cost.
    tail = t('{} signals checked this week, {} still waiting', f'{reviewed:,}', f'{backlog:,}') if backlog else t('{} signals checked this week', f'{reviewed:,}')
    lines += ['', '_' + t('Behind the scenes: {}.', tail) + '_']

    # 5. One-tap choices, each its own message with its own buttons, so it reads without scrolling back: nothing
    # changes until the owner taps, and a tap changes only their own filters or cards.
    items = []
    busy = [(k, v) for k, v in sorted(noise.items(), key=lambda kv: -kv[1]['n']) if k[0] and v['n'] >= 20 and v['rule'] not in kept_rules][:3]
    for (account, where), v in busy:
        items.append({'kind': 'noise', 'ref': account, 'data': {'account': account, 'rule': v['rule'], 'label': f'{where} ({names.get(account, account)})'},
                      'line': '**' + t('Busy without results') + f"**\n{recap_escape(where)} ({recap_escape(names.get(account, account))}): "
                              + t('{} this week, no to-dos', f"{v['n']:,}")})
    again = [s for s in snoozed if s['id'] in open_cards and not (s['id'] in kept_cards and s['last'] <= kept_cards[s['id']])][:3]
    for s in again:
        items.append({'kind': 'snoozed', 'ref': s['id'], 'data': {'title': open_cards[s['id']]['title']},
                      'line': '**' + t('Snoozed more than once') + f"**\n{link(recap_clip(open_cards[s['id']]['title']), s['id'])}, " + t('{} times', s['n'])})
    for n, item in enumerate(items, 1):
        item.update(id='r_' + secrets.token_hex(6), n=n, status='open')
    return {'text': '\n'.join(lines), 'items': items}


RECAP_CHOICES_NOTE = 'Choices follow below. Nothing changes until you tap.'
RECAP_MAIL_SUBJECT = 'Your week with The Machine'


def recap_mail_text(text):
    """The recap as a plain email: its lines kept, bold and italics dropped, a link as its words with the address after."""
    out = []
    for line in str(text or '').split('\n'):
        kept = []  # what recap_escape escaped is the owner's own text: kept as written
        line = re.sub(r'\\(.)', lambda m: kept.append(m.group(1)) or f'\x00{len(kept) - 1}\x00', line)
        line = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'\1 (\2)', line)
        line = re.sub(r'\*\*|(?<!\w)_|_(?!\w)', '', line)
        out.append(re.sub('\x00(\\d+)\x00', lambda m: kept[int(m.group(1))], line).rstrip())
    return '\n'.join(out).strip()


def weekly_recap(store, config, current=None):
    """The recap as the owner reads it on Telegram, its messages one after the other (without storing its choices)."""
    recap = weekly_recap_message(store, config, current)
    note = ['_' + i18n.t(RECAP_CHOICES_NOTE) + '_'] if recap['items'] else []
    return '\n\n'.join([recap['text'], *note, *(i['line'] for i in recap['items'])])


class RecapApp:
    # action name -> the method that handles it, called as method(name, args, owner_dashboard) (App.action)
    ACTIONS = {'recap_decide': 'recap_decide_action'}

    def recap_push(self, message, week):
        """Without Telegram the recap's start goes to the dashboard app as a notification: what needs the owner first."""
        with self.store.connect() as db:
            subscriptions = [dict(r) for r in db.execute('SELECT endpoint,p256dh,auth FROM push_subscriptions')]
            show = security_levels.notify_text(db)
        body = '\n'.join(message.split('\n')[1:])  # the title says it is the week; the first section leads
        if subscriptions and self.config.get('dashboard_host'):
            root = 'https://' + self.config['dashboard_host'] + self.config.get('dashboard_path', '/')
            try:
                push_node(self.config, {'action': 'send', 'subscriptions': subscriptions,
                                        'payload': {'title': i18n.t('Your week'), 'body': plain(body), 'url': root, 'tag': 'recap-' + week,
                                                    'actions': quick_web('view')}})
            except (subprocess.TimeoutExpired, ValueError, KeyError) as error:
                LOG.warning('push recap error=%s', type(error).__name__)
        try:
            app_wake(self.store, self.config, 'digest', 'recap-' + week, line=i18n.t('Your week'),  # the app asks for both
                     detail=notify.clip(plain(body), notify.APP_BODY) if show else '')
        except Exception as error:  # noqa: BLE001 - best effort, like the web push
            LOG.warning('app push recap error=%s', type(error).__name__)
        return {'messageId': 'web-recap-' + week}

    def recap_mail(self, text, week, mail=None):
        """The recap by email too, when the owner's email notifications for the digest are on (Settings, Notifications),
        through the control plane's mailer like the digest. Not with Careful or notification text off: the text would
        pass the mailer in the clear. True when the mailer took it."""
        with self.store.connect() as db:
            notify.ensure(db)
            on, show = notify.allowed(db, 'digest', 'email'), security_levels.notify_text(db)
        target = on and show and self.notify_mail_target()
        if not target:
            if on:
                LOG.info('recap email skipped reason=%s', 'careful' if not show else 'not_paired')
            return False
        return bool((mail or notify.mail)(target[0], target[1], i18n.t(RECAP_MAIL_SUBJECT), recap_mail_text(text), delivery='recap-' + week))

    def recap_step(self, sender=None, current=None, mail=None):
        """Send the weekly recap once, Fridays from 16:00 (on unless the owner turned it off: recap_settings): the
        recap, then each choice as its own short message with its own buttons. Its choices are stored with it, so a tap
        on a button is checked against the message it came from. It goes on Telegram, else by push to the dashboard app
        and the phone, and also by email when the owner's email notifications are on (recap_mail). sender(message,
        buttons) and mail stand in for the delivery (tests)."""
        settings = recap_settings(self.config)
        if not settings.get('enabled'):
            return None
        current = current or dt.datetime.fromisoformat(now())
        local = current.astimezone(local_tz())
        if local.isoweekday() != settings.get('weekday', 5) or local.strftime('%H:%M') < settings.get('at', '16:00'):
            return None
        week = local.strftime('%G-W%V')
        with self.store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if db.execute('SELECT 1 FROM recaps WHERE week=?', (week,)).fetchone():
                return None
            db.execute("INSERT INTO recaps(week,status,created_at) VALUES(?,'sending',?)", (week, now()))
        recap = weekly_recap_message(self.store, self.config, current)
        text, items = recap['text'], recap['items']
        on_telegram = sender is not None or telegram_on(self.config)
        if not on_telegram:  # the dashboard app gets the text; its choices need Telegram's buttons
            items = []
        if items:
            text += '\n\n_' + i18n.t(RECAP_CHOICES_NOTE) + '_'
        with self.store.connect() as db:
            db.execute('UPDATE recaps SET text=? WHERE week=?', (text, week))
            for item in items:
                db.execute("INSERT INTO recap_items(id,week,n,kind,ref,line,data,status) VALUES(?,?,?,?,?,?,?,'open')",
                           (item['id'], week, item['n'], item['kind'], item['ref'], item['line'], encoded(item['data'])))
        if sender is None and not on_telegram:
            sender = lambda message, buttons: self.recap_push(message, week)
        sender = sender or (lambda message, buttons: telegram_request(self.config, {
            'action': 'send', 'channel': 'telegram', 'accountId': telegram_account(self.config), 'target': self.config.get('telegram_owner'),
            'message': message, 'presentation': recap_presentation(buttons)}))
        status, message_id, error = 'uncertain', None, None
        try:
            receipt = sender(text, [])
            message_id = receipt.get('messageId') or receipt.get('message_id')
            status = 'sent' if message_id else 'uncertain'
        except DeliveryNotSent as failure:
            status, error = 'not_sent', str(failure)
        except (subprocess.TimeoutExpired, ValueError):
            error = 'delivery_outcome_unknown'  # never resend blindly
        try:
            emailed = self.recap_mail(recap['text'], week, mail)  # without the note on Telegram's choices
        except Exception as failure:  # noqa: BLE001 - best effort, like the push
            LOG.warning('recap email error=%s', type(failure).__name__)
            emailed = False
        if emailed and status == 'not_sent':  # the email went: no second try next round
            status = 'sent'
        with self.store.connect() as db:
            if status == 'not_sent':
                db.execute('DELETE FROM recap_items WHERE week=?', (week,))
                db.execute('DELETE FROM recaps WHERE week=?', (week,))  # nothing went out; try again later
            else:
                db.execute('UPDATE recaps SET status=?,message_id=?,error=? WHERE week=?', (status, message_id, error, week))
        for item in items if status != 'not_sent' else []:
            # Each choice after the recap, as its own message with its own buttons. One that didn't go out (or may not
            # have) is forgotten, so a stray tap on it does nothing; it comes up again next week.
            try:
                receipt = sender(item['line'], recap_buttons([item]))
                sent_id = receipt.get('messageId') or receipt.get('message_id')
            except (DeliveryNotSent, subprocess.TimeoutExpired, ValueError):
                sent_id = None
            with self.store.connect() as db:
                if sent_id:
                    db.execute('UPDATE recap_items SET message_id=? WHERE id=?', (str(sent_id), item['id']))
                else:
                    db.execute('DELETE FROM recap_items WHERE id=?', (item['id'],))
        return status

    def recap_view(self, item_id):
        """What a tap's message shows now, and that message: a choice's own message, or for a recap sent before each
        choice had one, the whole recap with its numbered buttons."""
        with self.store.connect() as db:
            item = db.execute('SELECT * FROM recap_items WHERE id=?', (item_id,)).fetchone()
            row = item and db.execute('SELECT text,message_id FROM recaps WHERE week=?', (item['week'],)).fetchone()
            if item and item['message_id']:
                return recap_choice_view(dict(item)), item['message_id']
            items = [dict(r) for r in db.execute('SELECT * FROM recap_items WHERE week=? ORDER BY n', (item['week'],))] if row else []
        return (recap_view(row['text'] or '', items), row['message_id']) if row else (None, None)

    def recap_retell(self, item_id):
        """The message a tap came from brought up to date: the line says what was done, its buttons go."""
        try:
            view, message_id = self.recap_view(item_id)
            if view and message_id and telegram_on(self.config) and not str(message_id).startswith('web-'):
                telegram_request(self.config, {'action': 'edit', 'channel': 'telegram', 'accountId': telegram_account(self.config),
                                               'target': self.config.get('telegram_owner'), 'messageId': str(message_id),
                                               'message': view['text'], 'presentation': recap_presentation(view['buttons'])})
        except Exception as error:
            LOG.warning('recap edit error=%s', type(error).__name__)

    def recap_filter(self, data, add):
        """Add (or, for Undo, take out) one `exclude` rule on one of the owner's own accounts, in config.json and at
        once for new signals. Signals already stored stay; only new ones are skipped."""
        import onboarding
        if not getattr(self, 'config_path', None):
            raise ValueError('This can’t be changed on this Machine.')
        config = onboarding.load(self.config_path)
        account = next((x for x in config.get('accounts', []) if x.get('id') == data.get('account')), None)
        if not account or not isinstance(data.get('rule'), dict):
            raise ValueError('That source is no longer connected')
        rules = account.setdefault('exclude', [])
        if add and data['rule'] not in rules:
            rules.append(data['rule'])
        elif not add:
            account['exclude'] = [r for r in rules if r != data['rule']]
        onboarding.save(self.config_path, config)
        live = next((x for x in self.config.get('accounts', []) if x.get('id') == account['id']), None)
        if live is not None:
            live['exclude'] = account['exclude']
            self.store.exclusions[account['id']] = (live.get('exclude') or []) + default_exclusions(self.config, live)

    def recap_decide(self, args, owner_dashboard=False):
        """A tap on the weekly recap: Filter, Keep or Undo on a busy source; Not needed, Do it or Keep on a card snoozed
        again and again. Also Keep or Drop on a to-do's own "Still needed?" (still_needed.py), from the dashboard only.
        Only the owner's own filters and cards change; nothing is sent to anyone. From Telegram only on the recap
        message that offered it."""
        item_id, choice = str(args.get('id') or ''), str(args.get('choice') or '')
        if not owner_dashboard and args.get('source') != 'telegram':
            raise ValueError('Recap choices come from the recap message')
        with self.store.connect() as db:
            item = db.execute('SELECT i.*,r.message_id recap_message_id,r.week recap_week FROM recap_items i LEFT JOIN recaps r ON r.week=i.week WHERE i.id=?',
                              (item_id,)).fetchone()
        if not item or (item['kind'] != still_needed.KIND and item['recap_week'] is None):  # a recap's line needs its recap
            raise ValueError('That recap line is no longer known')
        item = dict(item)
        on_todo = item['kind'] == still_needed.KIND  # asked on the to-do, not in a recap message
        if on_todo and not owner_dashboard:
            raise ValueError('Still needed? is answered on the to-do')
        offered_in = item['message_id'] or item['recap_message_id']  # its own message, or the whole recap (sent before each choice had one)
        if not owner_dashboard and str(offered_in or '') != str(args.get('message_id') or ''):
            raise ValueError('That Telegram message is not the recap this line was sent in')
        if choice not in RECAP_CHOICES[item['kind']]:
            raise ValueError('Unknown choice')
        decision = str(args.get('decision_id') or '') or 'recap:' + secrets.token_hex(8)
        if item['decision_id'] == decision:
            return {'status': item['status'], 'duplicate': True}
        if (choice == 'undo') != (item['status'] == 'filtered') or (choice != 'undo' and item['status'] != 'open'):
            return {'status': item['status'], 'reason': i18n.t('Already done: {}.', i18n.t(RECAP_DONE.get(item['status'], 'Open')).lower())}
        data, status = json.loads(item['data']), {'filter': 'filtered', 'keep': 'kept', 'undo': 'open', 'drop': 'dropped', 'now': 'started'}[choice]
        source = 'dashboard' if owner_dashboard else 'telegram'
        if choice in ('filter', 'undo'):
            self.recap_filter(data, choice == 'filter')
            with self.store.connect() as db:
                db.execute("INSERT INTO rule_changes(at,kind,text,ref) VALUES(?,'filter',?,?)",
                           (now(), ('Filter: ' if choice == 'filter' else 'Removed filter: ') + data.get('label', ''), item['id']))
        elif choice in ('drop', 'now'):
            card = item['ref']
            with self.store.connect() as db:
                row = db.execute('SELECT status FROM suggestions WHERE id=?', (card,)).fetchone()
            if not row or row['status'] in ('completed', 'rejected'):
                status = 'dropped' if row and row['status'] == 'rejected' else 'kept'
                reason = 'That to-do is already closed.'
            else:
                reason = None
                if choice == 'drop':  # the dashboard's own Not needed
                    self.store.decide(card, 'reject', 'No longer needed' if on_todo else i18n.t('Marked not needed in the weekly recap'), decision + ':drop', source)
                else:  # Unsnooze, then Do it: preparing never sends anything without the owner's own tap on the card
                    result = self.store.decide(card, 'accept', '', decision + ':back', source) if row['status'] == 'snoozed' else {'status': row['status']}
                    if result.get('status') == 'pending':
                        self.store.decide(card, 'accept', '', decision + ':do', source)
            if reason:
                with self.store.connect() as db:
                    db.execute('UPDATE recap_items SET status=?,decision_id=?,decided_at=? WHERE id=?', (status, decision, now(), item['id']))
                if not on_todo:
                    threading.Thread(target=self.recap_retell, args=(item['id'],), daemon=True).start()
                return {'status': status, 'reason': reason}
        with self.store.connect() as db:
            db.execute('UPDATE recap_items SET status=?,decision_id=?,decided_at=? WHERE id=?', (status, decision, now(), item['id']))
        if not on_todo:  # a recap message shows what was done; a to-do just redraws
            threading.Thread(target=self.recap_retell, args=(item['id'],), daemon=True).start()
        return {'status': status}

    def recap_decide_action(self, name, args, owner_dashboard=False):
        # a tap on the weekly recap's Filter, Keep, Undo, Not needed or Do it
        return self.recap_decide(args, owner_dashboard)

    def still_needed_step(self, current=None):
        """Still needed? (still_needed.py): asks once on each open to-do nobody touched for a week, and ends the question
        of one that closed. current: an ISO time (tests)."""
        with self.store.connect() as db:
            return FirstLookStore.still_needed_ask(db, current or now(), lambda row: looks_done(row) or waits_on_others(row), local_tz())
