"""The Store's to-dos, part 1 (refactor PR 16): making and changing one. suggest makes or updates a to-do from a review,
update_card, rename, move, merge and the owner's own to-dos change it, and the sources and promises it rests on are kept
with it. The helpers above the mixin match a to-do to its thread, sources and owner. A mixin of Store (assistant.py),
like App's mixins. Moved out of assistant.py as is."""
import contextlib
import datetime as dt
import hashlib
import json
import re
import sqlite3
import uuid

import chat_files
import graph
import i18n
import locale_prefs
from machine.cards import current_title, delivery_time, group_sender
from machine.config import LOG
from machine.sources.calendar import calendar_owned, expiry_moment
from machine.sources.connectors import load_connector
from machine.store.review import CARD_OPEN, own_message
from machine.text import _address, clamp, encoded
from timeutil import local_tz, now
import todo_areas


def first_look_running(db):
    """A first look (a preview The Machine started by itself) is running."""
    return bool(db.execute("SELECT 1 FROM review_runs WHERE preview=1 AND auto=1 AND status IN ('starting','running','recovering')").fetchone())


def active_preview(db):
    """The owner's one-off first-run review (`assistant preview`), while it runs."""
    return db.execute("SELECT run_id,started_at FROM review_runs WHERE preview=1 AND status IN ('starting','running','recovering')").fetchone()


USE_MAIL_KINDS = ('gmail.message', 'ms_graph.message')
CHAT_ASK_CHARS = 60  # a chat ask is a tap, one short line (set_chat_asks)


def use_view(db, use_events):
    """The messages a stuck run asks to use (preparation use_event_ids), for the to-do's button: {'n', 'mail'}, or None."""
    ids = json.loads(use_events or '[]')
    if not ids:
        return None
    kinds = [r[0] for r in db.execute('SELECT kind FROM events WHERE deleted=0 AND id IN (' + ','.join('?' * len(ids)) + ')', ids)]
    return {'n': len(kinds), 'mail': all(k in USE_MAIL_KINDS for k in kinds)} if kinds else None


def use_line(n, mail):
    """The event line after the owner let a run use messages from another area: a whole sentence per case (i18n)."""
    return ('Added the email to this to-do' if n == 1 else 'Added the emails to this to-do') if mail else \
        ('Added the message to this to-do' if n == 1 else 'Added the messages to this to-do')


def source_kind(kind):
    if kind in SOURCE_KIND:
        return SOURCE_KIND[kind]
    plugin = load_connector(str(kind).split('.')[0]) if '.' in str(kind) else None
    return (getattr(plugin, 'KINDS', None) or {}).get(kind, 'signal')


def awaiting_key(event, owner_slack_ids=()):
    """Where to look for the follow-up to someone else's promise in this message; None when the
    message is the owner's own or not a conversation."""
    m = event['metadata'] if isinstance(event['metadata'], dict) else json.loads(event['metadata'])
    key = {'account_id': event['account_id'], 'kind': event['kind'], 'since': event['occurred_at']}
    if event['kind'] == 'gmail.message' and 'SENT' not in m.get('labels', []) and _address(m.get('from')):
        return {**key, 'thread_id': m.get('thread_id'), 'from': _address(m.get('from'))}
    if event['kind'] == 'slack.message' and m.get('user_id') and m['user_id'] not in owner_slack_ids:
        return {**key, 'channel_id': m.get('channel_id'), 'user_id': m['user_id']}
    if event['kind'] in ('whatsapp.message', 'telegram.message', 'linkedin.message', 'x.dm') and not m.get('from_me') and (m.get('chat_id') or m.get('conversation_id')):
        return {**key, 'conversation': m.get('chat_id') or m['conversation_id'], 'sender': m.get('sender_id') or m.get('from') or ''}
    return None


def awaiting_match(watch, event, owner_slack_ids=()):
    m = event['metadata'] if isinstance(event['metadata'], dict) else json.loads(event['metadata'])
    if watch['kind'] == 'gmail.message' and watch.get('promise'):
        return ('SENT' not in m.get('labels', []) and _address(m.get('from')) == watch.get('from') and
                (not watch.get('thread_id') or m.get('thread_id') == watch['thread_id']))
    if watch['kind'] == 'gmail.message' and watch.get('delegated'):
        return ('SENT' not in m.get('labels', []) and _address(m.get('from')) == watch['from'] and
                ((watch.get('thread_id') and m.get('thread_id') == watch['thread_id']) or (watch.get('reply_to') and watch['reply_to'] in (m.get('in-reply-to') or ''))))
    if watch['kind'] == 'gmail.message':
        return 'SENT' not in m.get('labels', []) and (m.get('thread_id') == watch.get('thread_id') or _address(m.get('from')) == watch['from'])
    if watch['kind'] == 'slack.message':
        return m.get('channel_id') == watch['channel_id'] and m.get('user_id') == watch['user_id']
    if m.get('from_me') or (m.get('chat_id') or m.get('conversation_id')) != watch['conversation']:
        return False
    # In a group chat only the person who promised counts.
    return not watch['sender'] or (m.get('sender_id') or m.get('from') or '') == watch['sender']


SOURCE_KIND = {'gmail.message': 'email', 'calendar.event': 'calendar', 'slack.message': 'Slack', 'teams.message': 'Teams',
               'salesflare.email': 'CRM email', 'salesflare.meeting': 'CRM meeting',
               'android.notification': 'phone', 'whatsapp.message': 'WhatsApp', 'telegram.message': 'Telegram',
               'gateway.alert': 'The Machine', 'machine.system_log': 'The Machine'}


def own_life_evidence(db, event_ids):
    """Whether everyone the owner was in touch with on this evidence is from their own life (graph.own_life: Family,
    Friends, a family or friend relation, or the owner's word): such a matter is Personal, whatever mailbox it came in on."""
    ids = [int(i) for i in event_ids or () if str(i).lstrip('-').isdigit()]
    if not ids:
        return False
    try:
        rows = db.execute(f"SELECT DISTINCT n.info FROM graph_events g JOIN graph_nodes n ON n.id=g.node_id WHERE g.direct=1 "
                          f"AND n.kind='person' AND g.event_id IN ({','.join('?' * len(ids))})", ids).fetchall()
    except sqlite3.Error:
        return False
    return bool(rows) and all(graph.own_life(json.loads(r[0] or '{}')) for r in rows)


def thread_keys(rows):
    """The conversations a set of signals belong to where one thread is one matter: an email thread, a Slack thread."""
    keys = set()
    for r in rows:
        m = r['metadata'] if isinstance(r['metadata'], dict) else json.loads(r['metadata'] or '{}')
        if r['kind'] == 'gmail.message' and m.get('thread_id'):
            keys.add(('mail', r['account_id'], str(m['thread_id'])))
        elif r['kind'] == 'slack.message' and m.get('channel_id') and m.get('thread_ts'):
            keys.add(('slack', r['account_id'], m['channel_id'], str(m['thread_ts'])))
    return keys


# A rename on a card: the review's title goes to title_suggested and theirs stays (two parameters, the same title).
KEEP_OWNER_TITLE = ("title=CASE WHEN title_source='user' THEN title ELSE ? END,"
                    "title_suggested=CASE WHEN title_source='user' THEN ? ELSE NULL END")
OWNER_WORDS_MAX, TITLE_OWNER_MAX = 2000, 200


def owner_title(words, limit=90):
    """A card's first title from what the owner typed: its first line, cut at a word."""
    line = words.split('\n', 1)[0].strip()
    if len(line) <= limit:
        return line
    cut = line[:limit - 1].rsplit(' ', 1)[0] if ' ' in line[:limit - 1] else line[:limit - 1]
    return cut.rstrip(' ,;:.-') + '…'


def owner_card_of(db, rows):
    """The card the owner made for one of these signals (their owner.card signal), or None."""
    ids = {json.loads(r['metadata']).get('card_id') if isinstance(r['metadata'], str) else r['metadata'].get('card_id')
           for r in rows if r['kind'] == 'owner.card'} - {None}
    if len(ids) > 1:
        raise ValueError('These are several cards the owner made: suggest about one at a time')
    return db.execute('SELECT * FROM suggestions WHERE id=?', (ids.pop(),)).fetchone() if ids else None


def same_thread_card(db, rows, days=60):
    """The latest card whose evidence is in the same email or Slack thread as these signals: a later message in a
    thread is the same matter, so it updates that card (open, snoozed, waiting) instead of starting another one.
    Done and dismissed cards count too, after open ones."""
    keys = thread_keys(rows)
    if not keys:
        return None
    since = (dt.datetime.fromisoformat(now()) - dt.timedelta(days=days)).isoformat()
    statuses = CARD_OPEN + ('completed', 'rejected')
    # A follow-up to-do (follow_ups.py) is about one nudge: it closes by itself when they reply, so their reply is a
    # new matter and never folds into it.
    cards = db.execute(f"SELECT * FROM suggestions WHERE status IN ({','.join('?' * len(statuses))}) AND (created_at>=? OR status IN ('pending','accepted','prepared','instructions','snoozed')) "
                       "AND id NOT IN (SELECT suggestion_id FROM follow_up_cards WHERE suggestion_id IS NOT NULL) "
                       "ORDER BY CASE WHEN status IN ('completed','rejected') THEN 1 ELSE 0 END,created_at DESC", (*statuses, since)).fetchall()
    for card in cards:
        ids = json.loads(card['event_ids'] or '[]')
        if not ids:
            continue
        evidence = db.execute('SELECT account_id,kind,metadata FROM events WHERE id IN (' + ','.join('?' * len(ids)) + ')', ids).fetchall()
        if thread_keys(evidence) & keys:
            return card
    return None


def promise_closed_at(db, card):
    """When a closed to-do was last marked done or not needed."""
    return db.execute("SELECT max(created_at) FROM decisions WHERE suggestion_id=? AND choice IN ('complete','reject')", (card['id'],)).fetchone()[0]


def owner_card_alike(db, own, rows, event_ids, project=None, limit=4):
    """Open cards that may be the same matter as a to-do the owner made: one holding the same evidence or in the same
    email or Slack thread as the signals the review links to it, or sharing their people or project
    (same_matter_cards). Only the reviewer can tell by meaning; a pair the owner kept apart is not asked again."""
    offer = json.loads(own['merge_offer'] or '{}') if 'merge_offer' in own.keys() else {}
    skip = {own['id'], *([offer.get('card_id')] if offer.get('kept') else [])}
    signals = [r for r in rows if r['kind'] != 'owner.card']
    ids, keys = {r['id'] for r in signals}, thread_keys(signals)
    found = {}
    if signals:
        for card in db.execute(f"SELECT id,title,status,event_ids FROM suggestions WHERE status IN ({','.join('?' * len(CARD_OPEN))}) "
                               'ORDER BY created_at DESC LIMIT 200', CARD_OPEN):
            if card['id'] in skip:
                continue
            held = [i for i in json.loads(card['event_ids'] or '[]') if isinstance(i, int)]
            same = bool(ids & set(held))
            if not same and keys and held:
                evidence = db.execute('SELECT account_id,kind,metadata FROM events WHERE id IN (' + ','.join('?' * len(held)) + ')', held).fetchall()
                same = bool(thread_keys(evidence) & keys)
            if same:
                found[card['id']] = {'id': card['id'], 'title': card['title'], 'status': card['status']}
    for card in same_matter_cards(db, event_ids, project, limit=limit + len(skip)):
        if card['id'] not in skip:
            found.setdefault(card['id'], card)
    return list(found.values())[:limit]


def same_matter_cards(db, event_ids, project=None, limit=4):
    """Open cards that may be about the same matter: they share the people a signal is directly about, or its
    project. Only the reviewer can tell by meaning, so these are asked about, never merged by themselves."""
    try:
        people = {p['id'] for p in graph.card_people(db, event_ids, limit=10)[0]}
    except (sqlite3.Error, ValueError, TypeError):
        people = set()
    found = []
    for card in db.execute(f"SELECT * FROM suggestions WHERE status IN ({','.join('?' * len(CARD_OPEN))}) ORDER BY created_at DESC LIMIT 200", CARD_OPEN):
        same_project = project and card['project'] and re.sub(r'\s+', ' ', str(project)).strip().lower() == card['project'].lower()
        shared = False
        if people and not same_project:
            try:
                shared = bool(people & {p['id'] for p in graph.card_people(db, json.loads(card['event_ids'] or '[]'), limit=10)[0]})
            except (sqlite3.Error, ValueError, TypeError):
                shared = False
        if same_project or shared:
            found.append({'id': card['id'], 'title': card['title'], 'status': card['status']})
        if len(found) >= limit:
            break
    return found


def source_line(rows):
    """One readable line about where a suggestion comes from, for the card."""
    rows = [r for r in rows if r['kind'] not in ('owner.card', 'machine.parked_fix')]  # the owner's own words ("Added by you"), an update's note
    if not rows:
        return None
    first = rows[0]  # The reviewer's main evidence (callers keep its order).
    more = [r for r in rows[1:] if r['kind'] != 'fleet.request']  # a Fleet request's own event is the card's text, not another source
    if first['kind'] != 'slack.message' and own_message(first):
        # The owner's own message (a "Waiting on" to-do leads with it): who it went to, by the name their messages carry
        m = first['metadata'] if isinstance(first['metadata'], dict) else json.loads(first['metadata'] or '{}')
        when = locale_prefs.day_text(dt.datetime.fromisoformat(first['occurred_at']).astimezone(local_tz()), lang='en')
        names = {}
        for r in rows:
            rm = r['metadata'] if isinstance(r['metadata'], dict) else json.loads(r['metadata'] or '{}')
            shown = re.sub(r'\s*<[^>]+>', '', str(rm.get('from') or '')).strip().strip('"')
            if _address(rm.get('from')) and shown and '@' not in shown:
                names[_address(rm.get('from'))] = shown
        to = _address(m.get('to'))
        them = (names.get(to) or re.sub(r'\s*<[^>]+>', '', str(m.get('to') or '').split(',')[0]).strip().strip('"') or to) if to else m.get('chat_name')
        line = source_kind(first['kind']) + (f' to {them}' if them else '') + f' · {when}'
    else:
        line = source_text(first)
    return 'Source: ' + line + (f' (+{len(more)} more)' if more else '')


def source_text(row):
    """What a signal is, who it is from and when ("email from Sam Lee · Mon 20 Oct"), for any kind, the owner's own
    to-do (owner.card) too."""
    when = locale_prefs.day_text(dt.datetime.fromisoformat(row['occurred_at']).astimezone(local_tz()), lang='en')
    if row['kind'] == 'owner.card':
        return f'to-do the owner added · {when}'
    m = row['metadata'] if isinstance(row['metadata'], dict) else json.loads(row['metadata'] or '{}')
    if row['kind'] == 'intercom.conversation':  # the customer by name, as an email shows its sender
        m = {**m, 'sender_display': m.get('sender_display') or m.get('contact_name') or m.get('from_name')}
    who = (m.get('sender_display') or m.get('from') or m.get('chat_name') or m.get('app_name')
           or (('#' + m['channel_name']) if m.get('channel_name') else '') or (m.get('crm_account') or {}).get('name') or '')
    who = group_sender(re.sub(r'\s*<[^>]+>', '', str(who)).strip().strip('"')) or None
    return source_kind(row['kind']) + (f' from {who}' if who else '') + f' · {when}'


class CardsStore:
    """Store methods that make and change to-dos."""

    def set_chat_asks(self, db, suggestion_id, asks):
        """The review's asks for a to-do: up to two short things the owner may want to say in its chat, specific to it
        ("Offer Tuesday 10:00 instead"), shown as taps over the message box (todos-chat-thread.js chatSuggestions).
        Written with the to-do in the same review turn, so no model call of their own. Anything else is dropped: none
        rather than a canned line. Each update replaces them, so they never outlive what the to-do says."""
        lines = [' '.join(a.split()) for a in asks if isinstance(a, str)] if isinstance(asks, list) else []
        lines = list(dict.fromkeys(a for a in lines if 0 < len(a) <= CHAT_ASK_CHARS))[:2]
        db.execute('UPDATE suggestions SET chat_asks=? WHERE id=?', (encoded(lines) if lines else None, suggestion_id))

    def suggest(self, dedupe_key, title, body, event_ids, when='now', digest_at='08:30', work=False, urgent=False, due=None, ahead=False, awaiting=None, project=None,
                card_id=None, separate=False, reopen=False, match=False, _db=None, suggestion_id=None, owner_step=None, expires_at=None, expires_what=None,
                company=None, personal=False):
        """A new card, or with match (the review) the existing card about the same matter brought up to date:
        card_id names the card the reviewer judged to be the same matter, separate says it is a different one.
        suggestion_id: the new card's id, when the caller made its evidence first (owner_card). owner_step: the step is
        one only the owner can do (True), one The Machine can do (False), or unchanged on an update (None).
        expires_at, expires_what: the moment the card's whole point is tied to, and what it is ("the meeting with Sam");
        once it has passed the card closes by itself (expire_passed).
        company: the review's word that the matter is for another of the owner's companies than the mailbox it came in
        on (todo_areas.owner_companies): the to-do gets that company's accounts and stays there, as after a move.
        personal: the review's word that the matter is the owner's own life (family, friends, home), also on a work
        mailbox; so is evidence whose people are all from the owner's own life (own_life_evidence). The to-do is
        Personal from the start (todo_areas.personal_accounts), never a Work Fleet's."""
        if _db is None:
            with self.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                return self.suggest(dedupe_key, title, body, event_ids, when, digest_at, work, urgent, due, ahead, awaiting, project,
                                    card_id, separate, reopen, match, _db=db, suggestion_id=suggestion_id, owner_step=owner_step,
                                    expires_at=expires_at, expires_what=expires_what, company=company, personal=personal)
        if not dedupe_key or not title or not body or not event_ids:
            raise ValueError('Evidence, title, body and stable dedupe_key are required')
        if due is not None:
            try:
                due = dt.date.fromisoformat(str(due)[:10]).isoformat()
            except ValueError:
                raise ValueError('due must be the deadline date as YYYY-MM-DD') from None
        if len(title) > 90 or len(body) > 700:
            raise ValueError('Keep it simple: title under 90 characters; body under 700 characters, about three short sentences. Keep event IDs and internal details out of the message.')
        placed = todo_areas.company_accounts(company, getattr(self, 'accounts', None) or []) if company is not None else None
        with contextlib.nullcontext(_db) as db:
            if company is None and (personal is True or own_life_evidence(db, event_ids)):
                company, placed = todo_areas.PERSONAL, todo_areas.personal_accounts(getattr(self, 'accounts', None) or [])
            existing = db.execute('SELECT * FROM suggestions WHERE dedupe_key=? OR id=(SELECT suggestion_id FROM suggestion_keys WHERE dedupe_key=?)',
                                  (dedupe_key, dedupe_key)).fetchone()
            if existing and (not match or set(event_ids) <= set(json.loads(existing['event_ids'] or '[]'))):
                return {'id': existing['id'], 'status': existing['status'], 'duplicate': True}
            rows = db.execute('SELECT id,account_id,kind,occurred_at,ingested_at,metadata FROM events WHERE deleted=0 AND id IN (' + ','.join('?' for _ in event_ids) + ')', event_ids).fetchall()
            if {r['id'] for r in rows} != set(event_ids):
                raise ValueError('Every evidence event must exist and be live')
            expiry = expiry_moment(expires_at, expires_what, sorted(rows, key=lambda r: event_ids.index(r["id"]))) \
                if expires_at is not None or expires_what is not None else None
            if all(r['kind'] == 'calendar.event' and not calendar_owned(json.loads(r['metadata'])) for r in rows):
                raise ValueError("That meeting is on someone else's calendar that the owner can see, and they aren't on it: "
                                 'not theirs, so no card for it')
            teams = self.team_inbox(db, rows)
            if teams and len(teams) == len(rows):
                raise ValueError(f"That mail only went to {sorted(set(teams.values()))[0]}, which the owner marked as the team's: "
                                 'others pick it up, so no card for it')
            taken = [a for a in self.intercom_assignments(db, rows).values() if isinstance(a, tuple)]
            if taken and len(taken) == len(rows):
                raise ValueError(f"That Intercom conversation is assigned to {taken[0][1] or 'a teammate'}, not the owner: "
                                 'theirs to answer, so no card for it')
            own = owner_card_of(db, rows) if match else None
            if own is not None and card_id is not None and card_id != own['id']:
                # The owner's card is theirs to merge: the review only asks.
                return self.offer_merge(db, own, card_id)
            if own is not None and not separate and own['status'] in CARD_OPEN:
                # The owner's new to-do may be one the review already made (a promise, a mail): the review judges by
                # meaning, as for any signal, and the owner is asked (offer_merge) rather than left with two.
                alike = owner_card_alike(db, own, rows, event_ids, project)
                if alike:
                    raise ValueError(f"Not saved yet. The owner made to-do {own['id']} themselves, and these open cards share its evidence, "
                                     'thread, people or project: '
                                     + '; '.join(f"{c['id']} \"{c['title']}\" ({c['status']})" for c in alike)
                                     + '. If it is the same matter (the same ask, commitment or event, in other words), call suggest again with '
                                       'card_id set to that card: the owner is asked whether to merge the two. '
                                       'If it is a different matter, call suggest again with separate:true.')
            watch = None
            if awaiting is not None:
                promise = next((r for r in rows if r['id'] == awaiting), None)
                watch = promise and awaiting_key(dict(promise), self.owner_user_ids)
                if not watch:
                    raise ValueError('awaiting_event_id must be one of event_ids: the email, Slack, WhatsApp, Telegram or LinkedIn message where someone else made the promise')
                if when in ('now', 'digest') and not due:
                    raise ValueError('A follow-up on someone else\'s promise needs due (their deadline) or when, so the card waits until then')
            target = None
            if own is not None:
                target = own  # the owner's own signal always fills in their card, never a second one
            elif card_id is not None and match:
                target = db.execute('SELECT * FROM suggestions WHERE id=?', (card_id,)).fetchone()
                if not target:
                    raise ValueError('card_id must be an existing card')
            elif existing:
                target = existing  # the same key with new evidence: that card again
            elif match and not separate and awaiting is None:
                target = same_thread_card(db, rows)
                if not target:
                    alike = same_matter_cards(db, event_ids, project)
                    if alike:
                        raise ValueError('Not saved yet. These open cards share people or the project with this signal: '
                                         + '; '.join(f"{c['id']} \"{c['title']}\" ({c['status']})" for c in alike)
                                         + '. If it is the same matter (the same ask, commitment or conversation, in other words), call suggest again with '
                                           'card_id set to that card: it gets the new evidence, title and body and comes back if it was waiting. '
                                           'If it is a different matter, call suggest again with separate:true.')
            if target:
                saved = self.update_card(db, target, dedupe_key, title, body, rows, event_ids, when, digest_at, work, urgent, due, ahead, project, reopen)
                if company and not target['area']:  # the review placed it with its company or in Personal; the owner's own move stands
                    db.execute('UPDATE suggestions SET account_ids=coalesce(?,account_ids),area=? WHERE id=?', (placed and encoded(placed), company, target['id']))
                if owner_step is not None and not saved.get('attached'):
                    db.execute('UPDATE suggestions SET owner_step=? WHERE id=?', (int(bool(owner_step)), target['id']))
                if expiry and not saved.get('attached'):
                    db.execute('UPDATE suggestions SET expires_at=?,expires_what=? WHERE id=?', (*expiry, target['id']))
                return saved
            if due:
                # A deadline within three days goes out now; one that the
                # weekend hold would reach too late counts as urgent.
                today = dt.datetime.fromisoformat(now()).astimezone(local_tz()).date()
                if awaiting is not None and when in ('now', 'digest'):
                    # Someone else's deadline: check the morning after it passed.
                    when = (dt.date.fromisoformat(due) + dt.timedelta(days=1)).isoformat() + 'T' + digest_at
                elif (dt.date.fromisoformat(due) - today).days <= 3:
                    when = 'now'
            deliver_after = delivery_time(when, digest_at, work=work, urgent=urgent)
            if due and awaiting is None and deliver_after and dt.datetime.fromisoformat(deliver_after).astimezone(local_tz()).date().isoformat() > due:
                urgent = True
                deliver_after = delivery_time(when, digest_at, work=work, urgent=True)
            # Saved by a preview review: shown on the dashboard only. Never sent (not now and not
            # as a backlog after --activate) and not prepared ahead while reviews are off; a first-look card
            # its reviewer wanted prepared is, once reviews are on (prepare_first_look).
            preview = bool(active_preview(db))
            if preview:
                wanted = ahead and first_look_running(db)
                ahead, deliver_after = False, None
            suggestion_id = suggestion_id or uuid.uuid4().hex[:16]
            db.execute('INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at,deliver_after,source_line,urgent,due,owner_step) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                       (suggestion_id, dedupe_key[:240], title[:300], body[:5000], encoded(event_ids),
                        encoded(placed or sorted({r['account_id'] for r in rows})), now(), deliver_after, source_line(sorted([dict(r) for r in rows],key=lambda r:event_ids.index(r['id']))), int(urgent), due,
                        int(bool(owner_step))))
            if expiry:
                db.execute('UPDATE suggestions SET expires_at=?,expires_what=? WHERE id=?', (*expiry, suggestion_id))
            if company:  # pinned there, as a move is: a later signal on another company's mailbox doesn't pull it back
                db.execute('UPDATE suggestions SET area=? WHERE id=?', (company, suggestion_id))
            db.execute('INSERT INTO deliveries(suggestion_id,status,updated_at) VALUES(?,?,?)',
                       (suggestion_id, 'previewed' if preview else 'queued', now()))
            if preview and wanted:
                db.execute('INSERT OR IGNORE INTO first_look_ahead(suggestion_id,created_at) VALUES(?,?)', (suggestion_id, now()))
            if watch:
                db.execute('UPDATE suggestions SET awaiting=? WHERE id=?', (encoded(watch), suggestion_id))
            if project:
                graph.label(db, event_ids, project, 'card', now())
                db.execute("UPDATE suggestions SET project=(SELECT name FROM projects WHERE name=? COLLATE NOCASE),project_by='review' WHERE id=? AND project_by IS NOT 'owner'",
                           (re.sub(r'\s+', ' ', str(project)).strip(), suggestion_id))
            graph.link_cards(db, [suggestion_id])
            if ahead:
                # Prepared ahead: the work starts now, research and drafting only, and the card
                # reaches the owner once it's ready. Sending or changing anything still waits for
                # their tap; if it can't finish, the card arrives as a normal suggestion.
                decision_id = 'ahead:' + suggestion_id
                db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                           (decision_id, suggestion_id, 'prepare_ahead', '', 'assistant', now()))
                db.execute("UPDATE suggestions SET status='accepted',early=1 WHERE id=?", (suggestion_id,))
                self.queue_preparation(db, suggestion_id, decision_id)
        return {'id': suggestion_id, 'status': 'accepted' if ahead else 'pending', 'duplicate': False, 'deliver_after': deliver_after,
                **({'prepared_ahead': True} if ahead else {}), **({'preview': True} if preview else {}),
                **({'awaiting': 'The card waits; if they follow up first it closes itself.'} if watch else {})}

    def update_card(self, db, card, dedupe_key, title, body, rows, event_ids, when, digest_at, work, urgent, due, ahead, project, reopen):
        """A new signal about a matter that already has a card. An open card gets the new evidence, title and body,
        and one that was snoozed or waiting for a reply comes back. A done or dismissed card only reopens when the
        reviewer says the matter needs the owner again (reopen) and a message from someone else arrived after it was
        closed, or a promise on it came due (reopen='due'); otherwise the signal is kept on it as evidence."""
        stamp, sid = now(), card['id']
        # The review's title; while the owner's own title holds (a rename) it waits in title_suggested for Reset.
        suggested, title = title, current_title(card, title)
        old_ids = json.loads(card['event_ids'] or '[]')
        ids = [*event_ids, *[i for i in old_ids if i not in event_ids]]  # the newest evidence leads the source line
        evidence = {r['id']: dict(r) for r in db.execute('SELECT id,account_id,kind,occurred_at,metadata FROM events WHERE id IN (' + ','.join('?' * len(ids)) + ')', ids)}
        accounts = sorted(set(json.loads(card['account_ids'] or '[]')) | {r['account_id'] for r in rows})
        if card['area']:  # moved by the owner (move_card): it stays in that area, whatever account the new signal came in on
            accounts = json.loads(card['account_ids'] or '[]')
        db.execute('INSERT OR IGNORE INTO suggestion_keys(dedupe_key,suggestion_id,created_at) VALUES(?,?,?)', (dedupe_key[:240], sid, stamp))
        added = [i for i in event_ids if i not in old_ids]
        closed = card['status'] in ('completed', 'rejected')
        own = card['origin'] == 'owner'
        # News is what reached the Machine after they made it: a calendar event's date can lie ahead and still be old context.
        if own and not any(r['kind'] != 'owner.card' and min(r['occurred_at'], r['ingested_at'] or r['occurred_at']) > card['created_at'] for r in rows):
            # The owner's own signal, or older context the review links to it: it fills in the card they made.
            # Not news, so the card stays where they put it (snoozed, done) and nothing is sent.
            return self.fill_owner_card(db, card, suggested, body, ids, accounts, [evidence[i] for i in ids if i in evidence], due, ahead and not closed, project, event_ids)
        if closed and reopen is True:
            # Done stays done unless something new happened after it was closed: a message from someone else that came
            # in later. Older signals the review only now reaches, and the owner's own sent reply, are kept as evidence.
            shut = promise_closed_at(db, card) or card['created_at']
            reopen = any(r['id'] in added and r['occurred_at'] > shut and not own_message(dict(r), self.owner_user_ids) for r in rows)
        if closed and not reopen:
            db.execute('UPDATE suggestions SET event_ids=?,account_ids=? WHERE id=?', (encoded(ids), encoded(accounts), sid))
            if added:
                db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                           ('update:' + uuid.uuid4().hex, sid, 'update', f'A later message was added: {title[:150]}', 'assistant', stamp))
            return {'id': sid, 'status': card['status'], 'duplicate': False, 'attached': True,
                    'note': 'Kept on the closed card as evidence; nothing was sent to the owner. If this genuinely needs the owner again, '
                            'call suggest again with card_id and reopen:true.'}
        if due and (dt.date.fromisoformat(due) - dt.datetime.fromisoformat(stamp).astimezone(local_tz()).date()).days <= 3:
            when = 'now'
        deliver_after = delivery_time(when, digest_at, work=work, urgent=urgent)
        if active_preview(db):
            if ahead and first_look_running(db):
                db.execute('INSERT OR IGNORE INTO first_look_ahead(suggestion_id,created_at) VALUES(?,?)', (card['id'], stamp))
            ahead, deliver_after = False, None
        waiting = card['status'] == 'snoozed'
        # New work on the matter: back to Outstanding as a fresh suggestion, or prepared ahead again.
        status = 'accepted' if ahead else 'pending' if waiting or closed or card['status'] in ('pending', 'prepared') else card['status']
        # A title the owner gave (a rename) stays: the review's goes to title_suggested. On their own card, their due date stays.
        db.execute('UPDATE suggestions SET ' + KEEP_OWNER_TITLE + ',body=?,event_ids=?,account_ids=?,source_line=?,deliver_after=?,urgent=?,'
                   + ('due=coalesce(due,?)' if own else 'due=coalesce(?,due)') + ',status=?,'
                   'early=?,outcome=CASE WHEN status=? THEN outcome ELSE NULL END,snoozed_until=NULL,resume_status=NULL,awaiting=NULL,handled_hint=NULL,undo_until=NULL,completed_from=NULL,'
                   'feedback_until=NULL,expires_at=CASE WHEN expired_at IS NULL THEN expires_at END,expired_at=NULL WHERE id=?',
                   (suggested[:300], suggested[:300], body[:5000], encoded(ids), encoded(accounts), source_line([evidence[i] for i in ids if i in evidence]),
                    deliver_after, int(urgent or bool(card['urgent'])), due, status, int(bool(ahead)), status, sid))
        was = (f"Updated with a new signal{' and brought back' if waiting else ' and reopened' if closed else ''}."
               + (f" Before: {card['title'][:150]}" if title[:300] != card['title'] else ''))
        db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                   ('update:' + uuid.uuid4().hex, sid, 'update', was, 'assistant', stamp))
        db.execute("UPDATE action_jobs SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status IN ('queued','blocked')", (stamp, sid))
        if project:
            graph.label(db, event_ids, project, 'card', stamp)
        if ahead:
            decision_id = 'ahead:' + uuid.uuid4().hex
            db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                       (decision_id, sid, 'prepare_ahead', '', 'assistant', stamp))
            db.execute("UPDATE preparations SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status='done'", (stamp, sid))
            self.queue_preparation(db, sid, decision_id)
        elif status == 'pending':
            db.execute("UPDATE preparations SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status IN ('queued','starting','running','blocked')", (stamp, sid))
        # One notification for the update, on the new suggestion's timing; the old message is edited to match.
        db.execute("INSERT INTO deliveries(suggestion_id,status,updated_at) VALUES(?,'queued',?) ON CONFLICT(suggestion_id) DO UPDATE SET "
                   "status=CASE WHEN status IN ('sending') THEN status ELSE 'queued' END,reminder=0,error=NULL,"
                   "needs_edit=CASE WHEN message_id IS NULL THEN needs_edit ELSE 1 END,updated_at=excluded.updated_at", (sid, stamp))
        return {'id': sid, 'status': status, 'duplicate': False, 'updated': True, 'deliver_after': deliver_after,
                **({'brought_back': True} if waiting else {}), **({'reopened': True} if closed else {}), **({'prepared_ahead': True} if ahead else {}),
                'note': 'The existing card was updated with this signal instead of a new card.'}

    def prepare_first_look(self, per_day, hours=24):
        """Reviews are on now: the first look's cards that its reviewer would have prepared ahead had reviews been on get
        prepared now (research and a draft, nothing sent), so the first card has its draft ready. Only while still
        untouched (pending, nothing decided by the owner), from the last `hours`, within the daily limit for preparing
        ahead (`per_day`, 0 drops them all). Returns how many."""
        since = (dt.datetime.fromisoformat(now()) - dt.timedelta(hours=hours)).isoformat()
        with self.connect() as db:
            if not db.execute('SELECT 1 FROM first_look_ahead LIMIT 1').fetchone():
                return 0
            db.execute('BEGIN IMMEDIATE')
            started = 0
            day = (dt.datetime.fromisoformat(now()) - dt.timedelta(days=1)).isoformat()
            for row in db.execute('SELECT f.suggestion_id,s.status,s.created_at FROM first_look_ahead f LEFT JOIN suggestions s ON s.id=f.suggestion_id '
                                  'ORDER BY f.created_at').fetchall():
                sid = row['suggestion_id']
                db.execute('DELETE FROM first_look_ahead WHERE suggestion_id=?', (sid,))
                touched = db.execute("SELECT 1 FROM decisions WHERE suggestion_id=? AND source!='assistant' LIMIT 1", (sid,)).fetchone()
                room = db.execute("SELECT count(*) FROM decisions WHERE choice='prepare_ahead' AND created_at>=?", (day,)).fetchone()[0] < per_day
                if row['status'] != 'pending' or touched or not room or (row['created_at'] or '') < since:
                    continue
                decision_id = 'ahead:' + uuid.uuid4().hex
                db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                           (decision_id, sid, 'prepare_ahead', '', 'assistant', now()))
                db.execute("UPDATE suggestions SET status='accepted',early=1 WHERE id=?", (sid,))
                self.queue_preparation(db, sid, decision_id)
                started += 1
        return started

    def based_on_check(self, db, event_id):
        """Refuses a based_on that isn't a live message from someone else, before anything is saved."""
        if isinstance(event_id, bool) or not isinstance(event_id, int):
            raise ValueError('based_on is the event id of the message the draft or decision follows')
        row = db.execute('SELECT id,kind,metadata FROM events WHERE id=? AND deleted=0', (event_id,)).fetchone()
        if not row:
            raise ValueError('based_on must be a live event')
        if row['kind'] == 'owner.card' or own_message(dict(row), self.owner_user_ids):
            raise ValueError("based_on is someone else's message (a teammate's input, another thread), not the owner's own")

    def mark_based_on(self, db, suggestion_id, event_id):
        """The message from someone else that a to-do's draft or decision follows (a teammate's input in Slack, another
        thread, a project note): the review's or the preparation's based_on. It joins the to-do's evidence after its main
        source, so Read message has it too, and the to-do shows it with a link ("Based on Sam in #ops", based_on_views)."""
        self.based_on_check(db, event_id)
        card = db.execute('SELECT event_ids FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
        if not card:
            raise ValueError('Unknown suggestion')
        ids = json.loads(card['event_ids'] or '[]')
        if event_id not in ids:
            ids.append(event_id)  # after the main source, which keeps leading the source line
        rows = {r['id']: dict(r) for r in db.execute('SELECT id,account_id,kind,occurred_at,metadata FROM events WHERE id IN ('
                                                    + ','.join('?' * len(ids)) + ')', ids)}
        db.execute('UPDATE suggestions SET based_on=?,event_ids=?,source_line=? WHERE id=?',
                   (event_id, encoded(ids), source_line([rows[i] for i in ids if i in rows]), suggestion_id))
        return {'based_on': event_id}

    def fill_owner_card(self, db, card, title, body, ids, accounts, evidence, due, ahead, project, event_ids):
        """The review's pass over a card the owner made: a clearer title (unless they renamed it), a body with the next
        step, people, threads and project, and a draft prepared ahead when it helps. Their words (owner_words), their
        due date and where the card is (snoozed, done) stay as they were; nothing is sent to anyone. One they gave no area
        (owner_card_area) goes where the messages the review linked to it are, when those are all in one area: that
        area's accounts, pinned there as after a move. Otherwise it keeps its accounts and the review's word places it."""
        stamp, sid = now(), card['id']
        pinned = None
        if not card['area'] and any(e['kind'] == 'owner.card' and json.loads(e['metadata'] or '{}').get('area_open') for e in evidence):
            mine = getattr(self, 'accounts', None) or []
            where = {a['id']: todo_areas.area_of_account(a) for a in mine}
            linked = {where.get(e['account_id']) for e in evidence if e['kind'] != 'owner.card'}
            known = {x['id'] for x in todo_areas.areas(mine)}
            if len(linked) == 1 and linked <= known:
                pinned = next(iter(linked))
                accounts = todo_areas.accounts_in(pinned, mine)
        # Done or dismissed, it keeps the title it had: Done shows what the to-do was, its status line how it ended.
        retitle = KEEP_OWNER_TITLE + ',' if card['status'] not in ('completed', 'rejected') else ''
        db.execute('UPDATE suggestions SET ' + retitle + 'body=?,event_ids=?,account_ids=?,source_line=?,due=coalesce(due,?) WHERE id=?',
                   ((title[:300], title[:300]) if retitle else ()) + (body[:5000], encoded(ids), encoded(accounts), source_line(evidence), due, sid))
        if pinned:
            db.execute('UPDATE suggestions SET area=? WHERE id=?', (pinned, sid))
        db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                   ('update:' + uuid.uuid4().hex, sid, 'update', f"Filled in by the review. Before: {card['title'][:150]}", 'assistant', stamp))
        if project:
            graph.label(db, event_ids, project, 'card', stamp)
            db.execute("UPDATE suggestions SET project=coalesce(project,(SELECT name FROM projects WHERE name=? COLLATE NOCASE)),project_by=coalesce(project_by,'review') WHERE id=? AND project_by IS NOT 'owner'",
                       (re.sub(r'\s+', ' ', str(project)).strip(), sid))
        ahead = bool(ahead) and card['status'] == 'pending' and not active_preview(db)
        if ahead:
            decision_id = 'ahead:' + uuid.uuid4().hex
            db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                       (decision_id, sid, 'prepare_ahead', '', 'assistant', stamp))
            db.execute("UPDATE suggestions SET status='accepted',early=1 WHERE id=?", (sid,))
            self.queue_preparation(db, sid, decision_id)
            # Ready, it reaches the owner like any card prepared ahead.
            db.execute("UPDATE deliveries SET status='queued',updated_at=? WHERE suggestion_id=? AND status='not_sent'", (stamp, sid))
        db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (sid,))
        return {'id': sid, 'status': 'accepted' if ahead else card['status'], 'duplicate': False, 'updated': True, 'owner_card': True,
                **({'prepared_ahead': True} if ahead else {}),
                'note': 'The owner made this card; it is filled in. Their own words stay on it.'}

    def offer_merge(self, db, own, other_id):
        """The review thinks the owner's card is the same as another one. Nothing merges: the card asks them."""
        other = db.execute('SELECT id,status FROM suggestions WHERE id=?', (other_id,)).fetchone()
        if not other:
            raise ValueError('card_id must be an existing card')
        offer = json.loads(own['merge_offer'] or '{}')
        if offer.get('card_id') == other_id and offer.get('kept'):
            return {'id': own['id'], 'status': own['status'], 'merge_offered': False,
                    'note': 'The owner keeps these two cards apart. Fill in their card on its own (card_id ' + own['id'] + ').'}
        if other['status'] in ('completed', 'rejected'):
            return {'id': own['id'], 'status': own['status'], 'merge_offered': False,
                    'note': 'That card is closed. Fill in the owner\'s card on its own (card_id ' + own['id'] + ').'}
        db.execute('UPDATE suggestions SET merge_offer=? WHERE id=?', (encoded({'card_id': other_id, 'at': now()}), own['id']))
        return {'id': own['id'], 'status': own['status'], 'merge_offered': True,
                'note': 'Not merged: the owner made this card, so they are asked whether it is the same as that one. '
                        'Other signals in this call were not saved; suggest them again without the owner\'s signal.'}

    def reviewed_event(self, account_id, source_id, kind, title, body, meta):
        """An event this Machine made itself (a time another Machine proposed, meet_app.py), marked reviewed so no
        review or preparation reads it by itself. The same source id is the same event. Returns its id."""
        stamp = now()
        with self.connect() as db:
            db.execute('INSERT OR IGNORE INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,deleted,content_hash,version,analyzed_version,ingested_at) '
                       'VALUES(?,?,?,?,?,?,?,0,?,1,1,?)',
                       (account_id, source_id, kind, stamp, title, body, json.dumps(meta), hashlib.sha256((title + body).encode()).hexdigest(), stamp))
            return db.execute('SELECT id FROM events WHERE account_id=? AND source_id=?', (account_id, source_id)).fetchone()[0]

    def owner_card(self, text, account_id, work=False, due=None, about=(), attach=(), project=None, files=None, due_at=None, area_open=False,
                   file_texts=None):
        """A card the owner makes themselves (New card on the dashboard). It goes through suggest() like every card, with
        their words as its first evidence: a signal of kind owner.card, left for the next review to fill in. Nothing is
        sent: the card is already on their screen (delivery not_sent) and its buttons need their tap as on any card.
        files: (draft key, file ids) the form uploaded (chat_files.py), kept with the to-do and given to its runs.
        area_open: the owner's area ids when they gave none and nothing on it points to one (owner_card_area): the review
        places it by what it is about (company or personal), or the message it follows up on does (fill_owner_card).
        With files, the words may be empty (a PDF shared from the phone): the first file's name is its title until the
        review fills it in from file_texts ({file id: text}, chat_files.texts), kept sealed with the event's metadata."""
        words = '\n'.join(' '.join(line.split()) for line in str(text or '').strip().splitlines()).strip()
        words = re.sub(r'\n{3,}', '\n\n', words)
        if not words and not (files and files[1]):
            raise ValueError('Say what needs doing')
        if len(words) > OWNER_WORDS_MAX:
            raise ValueError(f'Keep it under {OWNER_WORDS_MAX} characters')
        title = owner_title(words) if words else None
        stamp, sid = now(), uuid.uuid4().hex[:16]
        meta = {'from_me': True, 'sender_display': 'You', 'card_id': sid, 'origin': 'owner', **({'about': list(about)} if about else {}),
                **({'area_open': [str(x) for x in area_open][:8]} if area_open else {})}
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            body = words
            if title is None:  # only files: the first one's name as its title and their names as its text, until the review reads them
                names = [r['name'] for r in (db.execute('SELECT name FROM chat_files WHERE id=? AND suggestion_id=?', (str(i), files[0])).fetchone()
                                             for i in files[1][:chat_files.MAX_FILES]) if r]
                if not names:
                    raise ValueError('A file is gone. Add it again.')
                title = owner_title(' '.join(re.sub(r'\.[A-Za-z0-9]{1,5}$', '', names[0]).replace('_', ' ').split()) or names[0])
                body = ', '.join(names)
            cursor = db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,deleted,content_hash,version,analyzed_version,ingested_at) '
                                "VALUES(?,?,'owner.card',?,?,?,?,0,?,1,0,?)",
                                (account_id, 'owner:' + sid, stamp, title, words, json.dumps(meta), hashlib.sha256((words or title).encode()).hexdigest(), stamp))
            saved = self.suggest('owner:' + sid, title, clamp(body, 699), [cursor.lastrowid, *[i for i in attach if i != cursor.lastrowid]], when='now',
                                 work=work, due=due, project=project, _db=db, suggestion_id=sid)
            kept = chat_files.adopt(db, files[0], sid, files[1]) if files else []
            if kept:  # the review knows the to-do has them and what they say (its runs get the files themselves)
                read = file_texts or {}
                db.execute('UPDATE events SET metadata=? WHERE id=?', (json.dumps({**meta, 'files': [
                    {'name': f['name'], 'type': f['type'], **({'text': read[f['id']]} if read.get(f['id']) else {})} for f in kept]}), cursor.lastrowid))
            db.execute('UPDATE suggestions SET origin=?,owner_words=?,deliver_after=NULL,due_at=? WHERE id=?', ('owner', words, due_at, sid))
            db.execute("UPDATE deliveries SET status='not_sent',updated_at=? WHERE suggestion_id=?", (stamp, sid))
        return {'id': sid, 'status': saved['status'], 'title': title, 'event_id': cursor.lastrowid, **({'files': kept} if kept else {})}

    def report_seen(self, ids):
        """The owner saw what their confirmed steps did (Just done, Got it): those to-dos stay only in Done."""
        ids = [str(i) for i in (ids if isinstance(ids, list) else []) if re.fullmatch(r'[A-Za-z0-9_-]{1,64}', str(i))][:100]
        if not ids:
            raise ValueError('Which to-dos did you see?')
        with self.connect() as db:
            seen = db.execute('UPDATE suggestions SET done_report=NULL WHERE done_report IS NOT NULL AND id IN ('
                              + ','.join('?' * len(ids)) + ')', ids).rowcount
        return {'seen': seen}

    def rename_card(self, suggestion_id, title=None, reset=False, decision_id=None, source='dashboard'):
        """The owner's own title for a card, kept in `title` (so every surface shows it) while the generated one waits in
        title_suggested; reviews and preparations update that one, never theirs. reset goes back to the suggested title."""
        if not re.fullmatch(r'[A-Za-z0-9_.:-]{1,200}', str(decision_id or '')):
            raise ValueError('Renames come from the owner’s controls')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if db.execute('SELECT 1 FROM decisions WHERE id=?', (decision_id,)).fetchone():
                row = db.execute('SELECT title,title_suggested FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
                return {'id': suggestion_id, 'title': row['title'] if row else None, 'duplicate': True}
            row = db.execute('SELECT title,title_suggested FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            if not row:
                raise ValueError('Unknown to-do')
            suggested = row['title'] if row['title_suggested'] is None else row['title_suggested']
            if reset:
                new = suggested
            else:
                new = ' '.join(str(title or '').split())
                if not new:
                    raise ValueError('Give the to-do a title')
                if len(new) > TITLE_OWNER_MAX:
                    raise ValueError(f'Keep the title under {TITLE_OWNER_MAX} characters')
            kept = None if new == suggested else suggested
            if new == row['title'] and kept == row['title_suggested']:
                return {'id': suggestion_id, 'title': new, 'renamed': kept is not None, 'unchanged': True}
            db.execute('UPDATE suggestions SET title=?,title_suggested=?,title_source=? WHERE id=?', (new, kept, 'auto' if kept is None else 'user', suggestion_id))
            db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                       (decision_id, suggestion_id, 'rename' if kept is not None else 'rename_reset', '', source, now()))
            # A card already in Telegram is edited to the new title.
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (suggestion_id,))
        return {'id': suggestion_id, 'title': new, 'renamed': kept is not None, **({'title_suggested': kept} if kept is not None else {})}

    def move_card(self, suggestion_id, area=None, decision_id=None, source='dashboard', undo=None):
        """The owner moves a to-do to another of their areas (todo_areas.py): Personal to Work at their company, or back.
        Its accounts become that area's, so what it may read and send from, its Work or Personal label, timing, sharing
        and handoffs all follow; the messages it came from stay where they are. undo: the decision id of the move to take
        back (its toast's Undo), which puts its accounts back as they were. A to-do whose run stopped to ask for this
        very move (preparation move_to) carries on by itself, as one does after its sign-in; any other stuck one keeps
        Try again. Returns {'id', 'area', 'label', 'line', 'decision_id', 'resumed'}."""
        if not re.fullmatch(r'[A-Za-z0-9_.:-]{1,200}', str(decision_id or '')):
            raise ValueError('Moves come from the owner’s controls')
        accounts = getattr(self, 'accounts', None) or []
        companies = sum(a['id'] != todo_areas.PERSONAL for a in todo_areas.areas(accounts))
        resume = False
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT s.id,s.status,s.account_ids,s.area,p.status prep,p.error,p.move_to FROM suggestions s '
                             'LEFT JOIN preparations p ON p.suggestion_id=s.id WHERE s.id=?', (suggestion_id,)).fetchone()
            if not row:
                raise ValueError('Unknown to-do')
            done = db.execute('SELECT area FROM card_moves WHERE decision_id=?', (decision_id,)).fetchone()
            if done:  # the same tap again
                return {'id': suggestion_id, 'area': done['area'], 'label': todo_areas.label(done['area'], companies), 'duplicate': True}
            if row['status'] in ('completed', 'rejected'):
                raise ValueError('Reopen it first')
            if undo is not None:
                last = db.execute('SELECT * FROM card_moves WHERE suggestion_id=? AND undone_at IS NULL ORDER BY created_at DESC,rowid DESC LIMIT 1',
                                  (suggestion_id,)).fetchone()
                if not last or last['decision_id'] != undo:
                    raise ValueError('That move can’t be undone any more')
                ids, pinned = json.loads(last['accounts_before']), last['area_before']
                area = todo_areas.current(ids, accounts, pinned) or todo_areas.PERSONAL
                db.execute('UPDATE card_moves SET undone_at=? WHERE decision_id=?', (now(), undo))
            else:
                area = todo_areas.check(area, row['account_ids'], accounts, row['area'])
                ids, pinned = todo_areas.accounts_in(area, accounts), area
                if not ids:
                    raise ValueError('Pick one of your areas')
                resume = (row['prep'] == 'blocked' and not row['error'] and row['move_to'] == area
                          and row['status'] in ('pending', 'accepted', 'instructions'))  # pending: a prepared-ahead run's blocker
            db.execute('INSERT INTO card_moves(decision_id,suggestion_id,area,accounts_before,area_before,created_at) VALUES(?,?,?,?,?,?)',
                       (decision_id, suggestion_id, area, row['account_ids'] or '[]', row['area'], now()))
            if undo is not None:  # an undo is no move of its own to undo later
                db.execute('UPDATE card_moves SET undone_at=created_at WHERE decision_id=?', (decision_id,))
            db.execute('UPDATE suggestions SET account_ids=?,area=? WHERE id=?', (encoded(ids), pinned, suggestion_id))
            db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                       (decision_id, suggestion_id, 'move_undo' if undo is not None else 'move', '', source, now()))
            # Its Telegram card shows the other area's text rules (Careful hides card text on a lock screen for Work)
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (suggestion_id,))
        line = todo_areas.moved_line(area, companies)
        out = {'id': suggestion_id, 'area': area, 'label': todo_areas.label(area, companies), 'decision_id': decision_id,
               'line': i18n.t(*line) if isinstance(line, tuple) else i18n.t(line), 'resumed': False}
        if resume:
            try:
                self.decide(suggestion_id, 'retry', '', 'moved:' + decision_id, 'moved')  # no Try again line: they tapped the move
                out['resumed'] = True
            except ValueError as error:
                LOG.info('move resume skipped suggestion=%s error=%s', suggestion_id, error)
        return out

    def use_sources(self, suggestion_id, decision_id, source='dashboard'):
        """The owner's tap on "Use this email for this to-do": the messages its stuck run asked for (preparation_blocked
        use_event_ids) become its sources, so the run reads them like the ones it came from, and it carries on by itself.
        Only those messages: its accounts and area stay as they are. Returns {'id', 'line', 'resumed'}."""
        if not re.fullmatch(r'[A-Za-z0-9_.:-]{1,200}', str(decision_id or '')):
            raise ValueError('This comes from the owner’s controls')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            done = db.execute('SELECT event_ids,mail FROM card_uses WHERE decision_id=?', (decision_id,)).fetchone()
            if done:  # the same tap again
                return {'id': suggestion_id, 'line': i18n.t(use_line(len(json.loads(done['event_ids'])), bool(done['mail']))), 'duplicate': True}
            row = db.execute('SELECT s.status,s.event_ids,p.status prep,p.error,p.use_events FROM suggestions s '
                             'LEFT JOIN preparations p ON p.suggestion_id=s.id WHERE s.id=?', (suggestion_id,)).fetchone()
            if not row:
                raise ValueError('Unknown to-do')
            asked = json.loads(row['use_events'] or '[]') if row['prep'] == 'blocked' and not row['error'] else []
            if not asked or row['status'] not in ('pending', 'accepted', 'instructions'):  # pending: a prepared-ahead run's blocker
                raise ValueError('Nothing is waiting for that on this to-do')
            live = [r['id'] for r in db.execute('SELECT id FROM events WHERE deleted=0 AND id IN (' + ','.join('?' * len(asked)) + ')', asked)]
            if not live:
                raise ValueError('Those messages are gone')
            view = use_view(db, encoded(live))
            ids = json.loads(row['event_ids'] or '[]')
            db.execute('UPDATE suggestions SET event_ids=? WHERE id=?', (encoded(ids + [i for i in asked if i in live and i not in ids]), suggestion_id))
            db.execute('INSERT INTO card_uses(decision_id,suggestion_id,event_ids,mail,created_at) VALUES(?,?,?,?,?)',
                       (decision_id, suggestion_id, encoded(live), int(view['mail']), now()))
            db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                       (decision_id, suggestion_id, 'use_sources', '', source, now()))
        out = {'id': suggestion_id, 'line': i18n.t(use_line(view['n'], view['mail'])), 'resumed': False}
        try:
            self.decide(suggestion_id, 'retry', '', 'used:' + decision_id, 'used')  # no Try again line: they tapped Use
            out['resumed'] = True
        except ValueError as error:
            LOG.info('use resume skipped suggestion=%s error=%s', suggestion_id, error)
        return out

    def merge_answer(self, suggestion_id, merge, decision_id, source='dashboard'):
        """The owner's answer to "Looks like the same as X. Merge?" on their card. Merge folds their card into X, which
        keeps its own work (a draft, a run) and takes on their words, their title if they gave one, and the evidence.
        Keep both stops the question for that pair."""
        if not re.fullmatch(r'[A-Za-z0-9_.:-]{1,200}', str(decision_id or '')):
            raise ValueError('Merges come from the owner’s controls')
        stamp = now()
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            own = db.execute('SELECT * FROM suggestions WHERE id=?', (suggestion_id,)).fetchone()
            offer = json.loads((own['merge_offer'] if own else None) or '{}')
            if not own or not offer.get('card_id') or offer.get('kept'):
                raise ValueError('There is nothing to merge on this to-do')
            if db.execute('SELECT 1 FROM decisions WHERE id=?', (decision_id,)).fetchone():
                return {'id': suggestion_id, 'duplicate': True}
            other = db.execute('SELECT * FROM suggestions WHERE id=?', (offer['card_id'],)).fetchone()
            if not merge or not other or other['status'] in ('completed', 'rejected'):
                db.execute('UPDATE suggestions SET merge_offer=? WHERE id=?', (encoded({**offer, 'kept': True}), suggestion_id))
                db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                           (decision_id, suggestion_id, 'keep_both', '', source, stamp))
                return {'id': suggestion_id, 'merged': False}
            ids = json.loads(other['event_ids'] or '[]')
            ids += [i for i in json.loads(own['event_ids'] or '[]') if i not in ids]
            accounts = sorted(set(json.loads(other['account_ids'] or '[]')) | set(json.loads(own['account_ids'] or '[]')))
            words = '\n\n'.join(w for w in (other['owner_words'], own['owner_words']) if w)
            renamed = own['title_suggested'] is not None and other['title_suggested'] is None
            db.execute('UPDATE suggestions SET event_ids=?,account_ids=?,origin=?,owner_words=?,due=coalesce(?,due),project=coalesce(project,?) WHERE id=?',
                       (encoded(ids), encoded(accounts), 'owner', words or None, own['due'], own['project'], other['id']))
            if renamed:
                db.execute("UPDATE suggestions SET title_suggested=title,title=?,title_source='user' WHERE id=?", (own['title'], other['id']))
            db.execute('INSERT OR IGNORE INTO suggestion_keys(dedupe_key,suggestion_id,created_at) VALUES(?,?,?)', (own['dedupe_key'], other['id'], stamp))
            for event in db.execute("SELECT e.id,e.metadata FROM events e JOIN json_each(?) j ON j.value=e.id WHERE e.kind='owner.card'", (own['event_ids'],)).fetchall():
                meta = json.loads(event['metadata'])
                if meta.get('card_id') == own['id']:
                    db.execute('UPDATE events SET metadata=? WHERE id=?', (json.dumps({**meta, 'card_id': other['id']}), event['id']))
            chat_files.move(db, own['id'], other['id'])  # the files the owner made their to-do with
            db.execute("UPDATE suggestions SET status='rejected',closed_from=status,merge_offer=NULL WHERE id=?", (own['id'],))
            db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                       (decision_id, own['id'], 'merge', '', source, stamp))
            db.execute("UPDATE preparations SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status!='done'", (stamp, own['id']))
            db.execute("UPDATE action_jobs SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status IN ('queued','blocked')", (stamp, own['id']))
            db.execute("UPDATE deliveries SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status IN ('queued','not_sent')", (stamp, own['id']))
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id IN (?,?) AND message_id IS NOT NULL', (own['id'], other['id']))
        if own['owner_words'] and other['status'] in ('accepted', 'instructions', 'prepared'):
            # Work on X already started (a draft, a run): what the owner added is their note on it, so the draft takes it in
            self.decide(other['id'], 'other', own['owner_words'], decision_id + ':note', source)
        return {'id': other['id'], 'merged': True, 'from': own['id']}

    def ahead_room(self, per_day):
        since = (dt.datetime.fromisoformat(now()) - dt.timedelta(days=1)).isoformat()
        with self.connect() as db:
            # Automated follow-ups count apart (follow_ups.PER_DAY): they never use up the room for other to-dos
            return db.execute("SELECT count(*) FROM decisions WHERE choice='prepare_ahead' AND created_at>=? "
                              'AND suggestion_id NOT IN (SELECT suggestion_id FROM follow_up_cards)', (since,)).fetchone()[0] < per_day

    def settle_ahead(self, db):
        """A prepared-ahead card whose run got stuck goes to the owner as a new to-do instead. Its blocker stays
        (preparation blocked): the to-do shows "Needs your help" with the reason and questions, and Answer or Try
        again accepts it first and carries on (_decide)."""
        for row in db.execute("SELECT s.id FROM suggestions s JOIN preparations p ON p.suggestion_id=s.id WHERE s.early=1 AND s.status='accepted' AND p.status='blocked'").fetchall():
            db.execute("UPDATE suggestions SET status='pending',early=0 WHERE id=?", (row['id'],))
            # It goes out as the card itself, not as a reminder: also when an earlier notification exists (a card reopened by a new signal).
            db.execute("UPDATE deliveries SET reminder=0 WHERE suggestion_id=?", (row['id'],))

    def settle_awaiting(self, db):
        """A follow-up on someone else's promise closes itself when they wrote again before it was due.
        Their new message goes through the normal review, so a delay still gets a card."""
        for row in db.execute("SELECT s.id,s.awaiting FROM suggestions s JOIN deliveries d ON d.suggestion_id=s.id WHERE s.awaiting IS NOT NULL "
                              "AND d.message_id IS NULL AND d.status='queued' AND s.status IN ('pending','accepted','prepared','instructions')").fetchall():
            watch = json.loads(row['awaiting'])
            answer = next((e for e in db.execute('SELECT id,account_id,kind,occurred_at,title,metadata FROM events WHERE account_id=? AND kind=? AND occurred_at>? AND deleted=0 ORDER BY occurred_at',
                                                 (watch['account_id'], watch['kind'], watch['since'])) if awaiting_match(watch, dict(e), self.owner_user_ids)), None)
            if not answer:
                continue
            stamp = now()
            db.execute("UPDATE suggestions SET status='completed',early=0 WHERE id=?", (row['id'],))
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)",
                       ('followed-up:' + row['id'], row['id'], 'complete', f"They followed up: {answer['title'][:150]} (signal {answer['id']})", 'assistant', stamp))
            db.execute("UPDATE deliveries SET status='cancelled',reminder=0,updated_at=? WHERE suggestion_id=?", (stamp, row['id']))
            db.execute("UPDATE preparations SET status='cancelled',updated_at=? WHERE suggestion_id=? AND status IN ('queued','starting','running','blocked')", (stamp, row['id']))
        # A task handed to someone closes when they answer; their answer is reviewed as a reply to
        # this card, so anything left for the owner gets a new card.
        for row in db.execute("SELECT id,awaiting FROM suggestions WHERE status IN ('snoozed','prepared') AND json_extract(awaiting,'$.delegated')=1").fetchall():
            watch = json.loads(row['awaiting'])
            answer = next((e for e in db.execute('SELECT id,account_id,kind,occurred_at,title,metadata FROM events WHERE account_id=? AND kind=? AND occurred_at>? AND deleted=0 ORDER BY occurred_at',
                                                 (watch['account_id'], watch['kind'], watch['since'])) if awaiting_match(watch, dict(e), self.owner_user_ids)), None)
            if not answer:
                continue
            stamp = now()
            db.execute("UPDATE suggestions SET status='completed',completed_from='prepared',snoozed_until=NULL,resume_status=NULL,awaiting=? WHERE id=?",
                       (encoded({**watch, 'answered': answer['title'][:150]}), row['id']))
            db.execute("INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)",
                       ('answered:' + row['id'], row['id'], 'complete', f"{watch['name']} replied: {answer['title'][:150]} (signal {answer['id']})", 'assistant', stamp))
            db.execute("UPDATE deliveries SET reminder=0,needs_edit=1,updated_at=? WHERE suggestion_id=?", (stamp, row['id']))
            db.execute("UPDATE deliveries SET status='cancelled' WHERE suggestion_id=? AND status='queued'", (row['id'],))
