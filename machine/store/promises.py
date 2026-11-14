"""The Store's promises (refactor PR 17): what the owner and others said they'd do. Saving and settling a promise, when
one is checked, the promises page and the ones that slipped. A mixin of Store (assistant.py), like App's mixins. Moved
out of assistant.py as is."""
import datetime as dt
import json
import re
import sqlite3
import uuid

import follow_ups
import graph
import i18n
import locale_prefs
from machine.sources.slack import slack_ids_named, slack_name_table
from machine.store import graph_identifiers
from machine.store.cards import awaiting_key, awaiting_match, same_thread_card
from machine.store.review import AUTOMATED_LABELS, CARD_OPEN, own_message, ROBOT_SENDER
from machine.store.voices import OWN_KINDS
from machine.text import _address, encoded
import memory_use
from timeutil import local_tz, now
from machine import todo_states


# When an open promise is checked without a date: the owner's own after 3 days, someone else's after a week.
PROMISE_CHECK_DAYS = {'mine': 3, 'theirs': 7}


def promise_check_at(direction, due, made_at, digest_at='08:30', current=None):
    """When an open promise is checked: the owner's own the morning before it's due, so its to-do comes with a day to
    get it done (never sooner than three hours from now), someone else's the morning after; undated ones after
    PROMISE_CHECK_DAYS."""
    current = current or dt.datetime.fromisoformat(now())
    hour, minute = (int(x) for x in digest_at.split(':'))
    if due:
        day = dt.date.fromisoformat(due) + dt.timedelta(days=1 if direction == 'theirs' else -1)
    else:
        day = dt.datetime.fromisoformat(made_at).astimezone(local_tz()).date() + dt.timedelta(days=PROMISE_CHECK_DAYS[direction])
    target = dt.datetime.combine(day, dt.time(hour, minute), local_tz())
    if direction == 'mine':
        target = max(target, current + dt.timedelta(hours=3))
    return target.astimezone(dt.timezone.utc).isoformat()


def before_blocked(db, event_id, check_at, digest_at='08:30', thread=True):
    """Someone else's promise that an open to-do with a deadline waits on (a to-do holding the promise's message, or with
    thread the one in its thread): checked the morning before that deadline when that is sooner (never sooner than three
    hours from now), so the chase comes while it can still help. check_at as it was otherwise."""
    marks = ','.join('?' * len(CARD_OPEN))
    dues = [r['due'] for r in db.execute(f"SELECT s.due,s.dedupe_key FROM suggestions s, json_each(s.event_ids) j WHERE j.value=? AND s.status IN ({marks}) "
                                         "AND s.due IS NOT NULL", (event_id, *CARD_OPEN)) if not r['dedupe_key'].startswith('promise:')]
    if not dues and thread:
        row = db.execute('SELECT id,account_id,kind,metadata FROM events WHERE id=?', (event_id,)).fetchone()
        card = row and same_thread_card(db, [row])
        if card and card['status'] in CARD_OPEN and card['due'] and not card['dedupe_key'].startswith('promise:'):
            dues = [card['due']]
    try:
        deadline = min(dt.date.fromisoformat(str(d)[:10]) for d in dues) if dues else None
    except ValueError:
        return check_at
    if not deadline:
        return check_at
    hour, minute = (int(x) for x in digest_at.split(':'))
    target = max(dt.datetime.combine(deadline - dt.timedelta(days=1), dt.time(hour, minute), local_tz()),
                 dt.datetime.fromisoformat(now()) + dt.timedelta(hours=3))
    return target.astimezone(dt.timezone.utc).isoformat() if target < dt.datetime.fromisoformat(check_at) else check_at


def promise_logged(db, promise_id, kind, detail=None):
    db.execute('INSERT INTO promise_log(promise_id,at,kind,detail) VALUES(?,?,?,?)', (promise_id, now(), kind, None if detail is None else str(detail)))


def promise_state(row):
    """open, card (its card is out), kept, dropped or answered; a card closes the promise with it. A promise whose
    to-do is gone reads open again, so it never says "a to-do now" without one to open."""
    if row['status'] == 'carded':
        if not row.get('card_status'):
            return 'open'
        return {'completed': 'kept', 'rejected': 'dropped'}.get(row['card_status'], 'card')
    return row['status']


def promise_card(db, suggestion_id):
    """A promise's to-do as it stands now: the one the owner merged it into (merge_answer keeps its key there), else its
    own; None when there is none any more."""
    pick = 'SELECT id,status,dedupe_key,handled_hint,outcome,title FROM suggestions '
    card = db.execute(pick + 'WHERE id=?', (suggestion_id,)).fetchone() if suggestion_id else None
    seen = set()
    while card and card['status'] == 'rejected' and card['id'] not in seen:
        seen.add(card['id'])
        if not db.execute("SELECT 1 FROM decisions WHERE suggestion_id=? AND choice='merge'", (card['id'],)).fetchone():
            break
        into = db.execute(pick + 'WHERE id=(SELECT suggestion_id FROM suggestion_keys WHERE dedupe_key=? AND suggestion_id!=? ORDER BY created_at DESC LIMIT 1)',
                          (card['dedupe_key'], card['id'])).fetchone()
        if not into:
            break
        card = into
    return dict(card) if card else None


def promise_open_card(db, row):
    """A carded promise's to-do while it is still open (promise_card), as its whole row; else None."""
    card = promise_card(db, row['suggestion_id'])
    if not card or card['status'] not in CARD_OPEN:
        return None
    return dict(db.execute('SELECT * FROM suggestions WHERE id=?', (card['id'],)).fetchone())


def card_looks_done(card):
    """The Machine's word that a promise's open to-do is done (a later message showed it, or its run found it done):
    its reason, else None."""
    if not card or card['status'] in todo_states.CLOSED_OR_SNOOZED:
        return None
    try:
        hint = json.loads(card['handled_hint'] or 'null')
    except (TypeError, ValueError):
        hint = None
    try:
        outcome = json.loads(card['outcome'] or '{}')
    except (TypeError, ValueError):
        outcome = {}
    if not card['handled_hint'] and not (card['status'] == 'prepared' and isinstance(outcome, dict) and outcome.get('state') == 'already_done'):
        return None
    why = ' '.join(str(hint.get('reason') or '').split())[:160] if isinstance(hint, dict) else ''
    return i18n.t('The Machine saw it done: {}.', why.rstrip('.')) if why else i18n.t('The Machine saw it done.')


# A title too long for a to-do ends at a clause (", ", " and ", " then "...) or else a word, with an ellipsis, never
# mid-word or on a word that leaves the sentence hanging ("verify they still", "the number of").
TITLE_CLAUSE = re.compile(r'[,;]\s+|\s+(?:and|or|but|then|so|while|because|before|after|once|until)\s+|\s+[-–]\s+')


TITLE_DANGLING = frozenset('a an the and or but then so to of for with in on at by from into about as that which who '
                           'they it he she we you is are was be will would can could should may might still also how '
                           'many much more less if when while because before after once until not no their its his her my your our'.split())


def fit_title(text, limit=90, keep=0):
    """A to-do title that fits `limit` characters: as it is when it fits; else up to its last clause boundary that
    leaves a useful title (after the first `keep` characters, a prefix such as "Waiting on Sam: "), else up to a word,
    without hanging words at the end; '…' says it goes on."""
    text = ' '.join(str(text or '').split())
    if len(text) <= limit:
        return text
    room = text[:limit]  # the ellipsis takes one: a cut always ends before `limit`
    floor = max(keep + 12, limit * 2 // 5)
    cuts = [m.start() for m in TITLE_CLAUSE.finditer(room) if floor <= m.start() <= limit - 1]
    if cuts:
        cut = room[:cuts[-1]]
    else:
        cut = room[:limit - 1]
        cut = cut.rsplit(' ', 1)[0] if ' ' in cut[keep:] else cut
        words = cut.split(' ')
        while len(words) > 1 and len(' '.join(words)) > keep + 1 and words[-1].strip(',;:.-').casefold() in TITLE_DANGLING:
            words.pop()
        cut = ' '.join(words)
    return cut.rstrip(' ,;:.-–') + '…'


PROMISE_TITLE_MAX, PROMISE_WHAT_MAX = 90, 80


def promise_title(p, title):
    """A promise to-do's title, short enough for a to-do: cut at a clause (fit_title), after "Waiting on Sam: "."""
    keep = title.index(': ') + 2 if p['direction'] != 'mine' and ': ' in title else 0
    return fit_title(title, PROMISE_TITLE_MAX, keep)


# who as an identifier the review read off a message instead of a name: a WhatsApp number, a WhatsApp chat id, an address
WHO_WHATSAPP = re.compile(r'(?:wa:\+?|\+)?(\d{6,15})(?:@s\.whatsapp\.net)?')
WHO_ADDRESS = re.compile(r'(?:email:)?([^@\s:<>]+@[^@\s<>]+\.[^@\s<>]+)')


def identifier_named(db, who):
    """who by the person's name when it is only an identifier ("wa:32470000301", "ann@client.example"): the graph's
    person with it. A WhatsApp number no one is known for reads as a phone number, never the internal "wa:" form."""
    phone, address = WHO_WHATSAPP.fullmatch(who), WHO_ADDRESS.fullmatch(who)
    key = 'wa:' + phone[1] if phone else 'email:' + address[1].lower() if address else None
    if not key:
        return who
    try:
        row = db.execute("SELECT name FROM graph_nodes WHERE id=? AND kind='person'", (key,)).fetchone() or next(iter(
            graph_identifiers.rows(db, 'n.name,n.info', [key], "SELECT name,info FROM graph_nodes WHERE kind='person' AND info LIKE ?",
                                   ['%"' + key + '"%'])), None)
    except sqlite3.OperationalError:
        row = None  # no graph yet
    name = ' '.join(str(row[0] or '').split()) if row else ''
    if name and not WHO_WHATSAPP.fullmatch(name) and not WHO_ADDRESS.fullmatch(name):
        return name
    return '+' + phone[1] if phone else who


def who_named(db, who):
    """who as the dashboard and to-dos say it: by name, whatever the review knew them by (a Slack member id, a number)."""
    return identifier_named(db, slack_ids_named(db, who))


def promise_who_named(db, p):
    """The promise with who by the person's name ("Slack teammate U02AB3CD4" as "Sam Lee"), for its to-do's title and
    body. One whose name isn't known yet keeps the id, which is named when shown."""
    p = {**p, 'who': identifier_named(db, p['who'])}
    ids = graph.slack_ids_in(p['who'])
    names = slack_name_table(db, ids) if ids else {}
    return {**p, 'who': slack_ids_named(db, p['who'], names)} if ids and ids <= names.keys() else p


def promise_text(p):
    """A promise card's title and body. The title says what was promised; the body adds only who and when, in one
    short line, so the card never says the same thing twice."""
    made = dt.datetime.fromisoformat(p['made_at']).astimezone(local_tz())
    said = locale_prefs.day_text(made)
    due = dt.date.fromisoformat(p['due']) if p.get('due') else None
    # The due chip says when it is due; the line adds it only when it isn't the day it was said
    t = i18n.t  # written once, when the card is made: in the owner's language then
    by = due and due != made.date() and locale_prefs.day_text(due)
    if p['direction'] == 'mine':
        title = p['what'][:1].upper() + p['what'][1:]
        title = title if p['who'].lower() in title.lower() or len(title) + len(p['who']) > 84 else title + t(' for {}', p['who'])
        body = (t('Promised {} on {} for {}. Nothing shows it done yet.', p['who'], said, by) if by else
                t('Promised {} on {}. Nothing shows it done yet.', p['who'], said))
    else:
        title = t('Waiting on {}: {}', p['who'], p['what'])
        first = p['who'].split()[0] if p['who'].split() else p['who']
        # A Slack member not named yet ("Slack teammate U02AB3CD4"): its first word is no first name
        if len(title) > PROMISE_TITLE_MAX and first != p['who'] and not graph.slack_ids_in(p['who']):
            title = t('Waiting on {}: {}', first, p['what'])  # the person chip says who in full
        body = (t('Promised on {} for {}. Nothing has come in yet, so a short nudge may help.', said, by) if by else
                t('Promised on {}. Nothing has come in yet, so a short nudge may help.', said))
    return title, body


def retitle_cut_promises(db):
    """An open promise to-do whose title an older version cut off at 90 characters, mid-sentence ("... and verify
    they still"): the title it gets now (promise_title). Only while its title is still exactly that cut one: a
    rename (theirs or a review's) or another language since leaves it as it is."""
    rows = db.execute("SELECT s.id,s.title,p.direction,p.who,p.what,e.occurred_at made_at,p.due FROM suggestions s "
                      "JOIN promises p ON p.suggestion_id=s.id AND s.dedupe_key='promise:'||p.id JOIN events e ON e.id=p.event_id "
                      f"WHERE p.status='carded' AND s.title_source!='user' AND s.status IN ({','.join('?' * len(CARD_OPEN))})", CARD_OPEN).fetchall()
    for row in rows:
        p = dict(row)
        old = (p['what'][:1].upper() + p['what'][1:] if p['direction'] == 'mine' else i18n.t('Waiting on {}: {}', p['who'], p['what']))
        cut = len(old) > PROMISE_TITLE_MAX and row['title'] == old[:PROMISE_TITLE_MAX]
        # 2026-11-06: release 1231 made those whole with a Slack member's label as their name, its first word as
        # the first name ("Waiting on Slack: ..." for "Slack teammate U02AB3CD4"): those get the person's name
        label = p['who'].split()[0] if p['direction'] != 'mine' and graph.slack_ids_in(p['who']) and p['who'].split() else ''
        wrong = label and row['title'] == promise_title({**p, 'who': label}, promise_text({**p, 'who': label})[0])
        if not (cut or wrong):
            continue
        named = promise_who_named(db, p)
        title = promise_title(named, promise_text(named)[0])
        if title != row['title']:
            db.execute('UPDATE suggestions SET title=? WHERE id=?', (title, row['id']))
            db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (row['id'],))


class PromisesStore:
    """Store methods for promises."""

    def promise(self, args, digest_at='08:30'):
        """Record a promise from a reviewed message, or update an open one (id with status or due)."""
        if args.get('id') is not None:
            return self.update_promise(args, digest_at)
        direction = args.get('direction')
        if direction not in ('mine', 'theirs'):
            raise ValueError("direction is 'mine' (the owner promised) or 'theirs' (someone promised the owner)")
        who, what = ' '.join(str(args.get('who') or '').split()), ' '.join(str(args.get('what') or '').split())
        if not 2 <= len(who) <= 80 or not 3 <= len(what) <= PROMISE_WHAT_MAX:
            # `what` becomes the to-do's title: one short, whole action, never one cut to fit
            raise ValueError('who is the other person (2-80 characters); what is the promised action alone, starting with a verb, as it follows "they’d": "send the signed contract" (3-80 characters: say it shorter, never cut it off)')
        due = args.get('due')
        if due is not None:
            try:
                due = dt.date.fromisoformat(str(due)[:10]).isoformat()
            except ValueError:
                raise ValueError('due must be the promised date as YYYY-MM-DD, or left out when none was said') from None
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            event = db.execute('SELECT id,account_id,kind,occurred_at,metadata FROM events WHERE id=? AND deleted=0', (args.get('event_id'),)).fetchone()
            if not event or event['kind'] not in OWN_KINDS:
                raise ValueError('event_id is the email, Slack, WhatsApp, Telegram, LinkedIn or X message with the promise')
            own = own_message(dict(event), self.owner_user_ids)
            if direction == 'mine' and not own:
                raise ValueError("The owner's promises are in messages they sent (a reply, a yes or a reaction to a request); event_id is that message")
            # Only an email closes someone else's promise by itself: chats run on, so a later chat message from
            # them is no sign it was kept; the review closes those, or the check when it's due.
            watch = awaiting_key(dict(event), self.owner_user_ids) if direction == 'theirs' and event['kind'] == 'gmail.message' else None
            check_at = promise_check_at(direction, due, event['occurred_at'], digest_at)
            if direction == 'theirs':
                check_at = before_blocked(db, event['id'], check_at, digest_at)
            who = who_named(db, who)  # a sender the review only knew by an id or a number: their name
            stamp = now()
            # `what` is sealed under message protection (a fresh nonce each time), so the same promise is found by
            # opening this message's promises here, not by the UNIQUE constraint, which then never matches
            row = next((r for r in db.execute('SELECT id,status,what FROM promises WHERE event_id=? AND direction=? AND who=?',
                                              (event['id'], direction, who)) if r['what'] == what), None)
            if row:
                return {'id': row['id'], 'status': row['status'], 'duplicate': True}
            # A plan made together ("let's do it Sunday" and the yes to it) reads as a promise from both
            # sides, in two messages: one open promise with that person for the same thing is enough
            same = lambda r: ' '.join(r['what'].split()).casefold() == what.casefold()
            row = next((r for r in db.execute("SELECT p.id,p.status,p.what,p.direction,p.due,e.occurred_at made_at FROM promises p JOIN events e ON e.id=p.event_id "
                                              "WHERE p.status='open' AND p.who=? COLLATE NOCASE", (who,)) if same(r)), None)
            if row:
                if row['direction'] != direction:  # both sides said it: a plan made together, kept as the owner's
                    db.execute("UPDATE promises SET together=1,direction='mine',check_at=?,updated_at=? WHERE id=?",
                               (promise_check_at('mine', row['due'], row['made_at'], digest_at), stamp, row['id']))
                    promise_logged(db, row['id'], 'together', event['id'])
                return {'id': row['id'], 'status': row['status'], 'duplicate': True}
            cursor = db.execute('INSERT INTO promises(direction,who,what,due,check_at,event_id,account_id,watch,status,created_at,updated_at,owner_step) '
                                "VALUES(?,?,?,?,?,?,?,?,'open',?,?,?) ON CONFLICT(event_id,direction,who,what) DO NOTHING",
                                (direction, who, what, due, check_at, event['id'], event['account_id'], encoded({**watch, 'promise': True}) if watch else None, stamp, stamp,
                                 int(direction == 'mine' and args.get('owner_step') is True)))
        return {'id': cursor.lastrowid, 'status': 'open', 'check_at': check_at,
                'note': 'Recorded, no card. It is checked when due; if still open then, a card comes.'}

    def update_promise(self, args, digest_at='08:30', source='assistant'):
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT p.*,e.occurred_at made_at FROM promises p JOIN events e ON e.id=p.event_id WHERE p.id=?', (args.get('id'),)).fetchone()
            if not row:
                raise ValueError('Unknown promise id')
            if row['status'] == 'carded' and source == 'dashboard' and args.get('status') in ('kept', 'dropped'):
                return self.close_carded_promise(db, dict(row), args['status'])
            status, reason = args.get('status'), ' '.join(str(args.get('reason') or '').split())[:200]
            # A new date for a promise that is a to-do now moves both (move_promise): the same promise, never a second one
            live_card = row['status'] == 'carded' and not status and args.get('due') and source in ('assistant', 'dashboard') and promise_open_card(db, row)
            if row['status'] != 'open' and not live_card:
                raise ValueError('This promise is no longer open: its card is out, use looks_handled on that card' if row['status'] == 'carded' else 'This promise is no longer open')
            if status in ('kept', 'dropped'):
                if source == 'assistant' and len(reason) < 3:
                    raise ValueError('Say in a few words what shows it kept or no longer needed (reason), with the event_ids')
                db.execute('UPDATE promises SET status=?,note=?,updated_at=? WHERE id=?',
                           (status, reason or ('Done' if status == 'kept' else 'Not needed') + ' (you)', now(), row['id']))
                promise_logged(db, row['id'], status, source)
                return {'id': row['id'], 'status': status}
            if args.get('due') and source in ('assistant', 'dashboard'):
                try:
                    due = dt.date.fromisoformat(str(args['due'])[:10]).isoformat()
                except ValueError:
                    raise ValueError('due must be YYYY-MM-DD') from None
                newer = None
                if args.get('event_id') is not None:
                    newer = db.execute('SELECT id,occurred_at FROM events WHERE id=? AND deleted=0', (args['event_id'],)).fetchone()
                    if not newer:
                        raise ValueError('event_id is the newer message that gave the new date')
                note = reason or row['note'] if source == 'dashboard' else reason or None
                check_at = self.move_promise(db, dict(row), due, newer['id'] if newer else None, digest_at, note)
                return {'id': row['id'], 'status': row['status'], 'due': due, 'check_at': check_at}
        raise ValueError("Update a promise with status 'kept' or 'dropped' and a reason, or with a new due date")

    def move_promise(self, db, row, due, event_id=None, digest_at='08:30', note=None):
        """A promise given a new date (a later message rescheduled it, or the owner on the dashboard): its date and when
        it is checked follow, with a line in its history and the newer message as a source. One that is a to-do now
        moves that to-do too: its date, the newer message first in its sources, and someone else's goes out of sight
        until the morning after the new date (the check it would have had). Returns the new check_at."""
        check_at = promise_check_at(row['direction'], due, row['made_at'], digest_at)
        if row['direction'] == 'theirs':
            check_at = before_blocked(db, row['event_id'], check_at, digest_at)
        db.execute('UPDATE promises SET due=?,check_at=?,note=?,updated_at=? WHERE id=?', (due, check_at, note, now(), row['id']))
        promise_logged(db, row['id'], 'due', due)
        if event_id is not None and event_id != row['event_id']:
            promise_logged(db, row['id'], 'source', event_id)  # promise_page: the newer message, beside the first
        card = promise_open_card(db, row) if row['status'] == 'carded' else None
        if not card:
            return check_at
        ids = json.loads(card['event_ids'] or '[]')
        if event_id is not None and event_id not in ids:
            ids = [event_id] + ids
        db.execute('UPDATE suggestions SET due=?,event_ids=? WHERE id=?', (due, encoded(ids), card['id']))
        old_body, new_body = (promise_text(promise_who_named(db, {**row, 'due': d}))[1][:700] for d in (row['due'], due))
        if card['body'] == old_body:  # still the line it was made with: "Promised on ... for <the old date>"
            db.execute('UPDATE suggestions SET body=? WHERE id=?', (new_body, card['id']))
        db.execute('UPDATE deliveries SET needs_edit=1 WHERE suggestion_id=? AND message_id IS NOT NULL', (card['id'],))
        if row['direction'] == 'theirs' and not row.get('together') and card['status'] in todo_states.WAITING_ON_OWNER and check_at > now():
            self._decide(db, card['id'], 'snooze', i18n.t('Moved to {}', locale_prefs.day_text(dt.date.fromisoformat(due))),
                         'promise-moved:' + uuid.uuid4().hex, 'assistant', snoozed_until=check_at)
        return check_at

    def promise_twins(self, db, limit=3):
        """Open promises that may be an older one given again: the same person, the same direction, and an older promise
        still open or a to-do that is (a new date for it noted as a new promise, or stored before the review saw the
        older one). Only meaning tells whether it is the same thing, so the promise check reads each pair once
        (promise_twin_run); a pair it has read is logged as 'twin' on the newer one. [(newer, older)], oldest first."""
        rows = [dict(r) for r in db.execute("SELECT p.*,e.occurred_at made_at FROM promises p JOIN events e ON e.id=p.event_id "
                                            "WHERE p.status IN ('open','carded') AND e.deleted=0 ORDER BY e.occurred_at,p.id")]
        live = [r for r in rows if r['status'] == 'open' or promise_open_card(db, r)]
        asked = {}
        for r in db.execute("SELECT promise_id,detail FROM promise_log WHERE kind='twin'"):
            asked.setdefault(r['promise_id'], set()).add(str(r['detail']))
        pairs = []
        for i, newer in enumerate(live):
            if newer['status'] != 'open':
                continue  # one that is a to-do of its own stays as it is
            older = next((o for o in live[:i] if o['direction'] == newer['direction'] and o['who'].casefold() == newer['who'].casefold()
                          and str(o['id']) not in asked.get(newer['id'], ())), None)
            if older:
                pairs.append((newer, older))
        return pairs[:limit]

    def merge_twin(self, db, newer_id, older_id, digest_at='08:30'):
        """The newer promise is the older one given again: the older one keeps going (its to-do too), with the newer
        date and message (move_promise), and the newer one closes as the same as it. False when either changed since."""
        pick = 'SELECT p.*,e.occurred_at made_at FROM promises p JOIN events e ON e.id=p.event_id WHERE p.id=?'
        newer, older = (db.execute(pick, (i,)).fetchone() for i in (newer_id, older_id))
        if not newer or not older or newer['status'] != 'open' or not (older['status'] == 'open' or promise_open_card(db, older)):
            return False
        older = dict(older)
        if newer['due'] and newer['due'] != older['due']:
            self.move_promise(db, older, newer['due'], newer['event_id'], digest_at, older['note'])
        else:
            promise_logged(db, older['id'], 'source', newer['event_id'])
        db.execute("UPDATE promises SET status='dropped',note=?,updated_at=? WHERE id=?", (f"The same as promise {older['id']}", now(), newer['id']))
        promise_logged(db, newer['id'], 'merged', older['id'])
        return True

    def close_carded_promise(self, db, row, status):
        """The owner's Done or Drop on a promise that is a to-do now: its to-do closes with it (Done, or Not needed), so
        the two never disagree. One whose to-do is gone closes by itself."""
        card = promise_card(db, row['suggestion_id'])
        if card and card['status'] not in todo_states.CLOSED:
            self._decide(db, card['id'], 'complete' if status == 'kept' else 'reject', '', 'promise-close:' + uuid.uuid4().hex, 'dashboard')
        elif card and {'completed': 'kept', 'rejected': 'dropped'}[card['status']] != status:
            raise ValueError('Its to-do is closed already. Open the to-do to change that.')
        if not card:
            db.execute('UPDATE promises SET status=?,note=?,updated_at=? WHERE id=?',
                       (status, ('Done' if status == 'kept' else 'Not needed') + ' (you)', now(), row['id']))
        promise_logged(db, row['id'], status, 'dashboard')
        return {'id': row['id'], 'status': status, **({'card': card['id']} if card else {})}

    def close_seen_done(self, db):
        """A promise whose to-do The Machine saw done (looks_handled, or its run found it done): the to-do goes to Done
        and the promise closes as kept, with a short line saying so. The owner can reopen the to-do from Done."""
        for row in db.execute("SELECT id,suggestion_id FROM promises WHERE status='carded' AND suggestion_id IS NOT NULL").fetchall():
            card = promise_card(db, row['suggestion_id'])
            line = card_looks_done(card)
            if not line:
                continue
            try:
                seen_at = (json.loads(card['handled_hint'] or 'null') or {}).get('at') or ''
            except (TypeError, ValueError, AttributeError):
                seen_at = ''
            # The owner's own word since (Reopen, Undo, Not done) stands: theirs to close
            if db.execute("SELECT 1 FROM decisions WHERE suggestion_id=? AND choice IN ('reopen','undo','not_done') AND created_at>=?",
                          (card['id'], seen_at)).fetchone():
                continue
            self._decide(db, card['id'], 'complete', line, 'promise-seen:' + uuid.uuid4().hex, 'assistant')
            db.execute('UPDATE promises SET note=?,updated_at=? WHERE id=?', (line, now(), row['id']))
            promise_logged(db, row['id'], 'seen', card['id'])

    def settle_promises(self, db):
        """Someone else's email promise closes when that sender replies in the same thread (address only
        when the original has no thread): their new message is reviewed as usual. A promise whose message was deleted is dropped."""
        db.execute("UPDATE promises SET status='dropped',note='The message was deleted',updated_at=? WHERE status='open' "
                   "AND event_id IN (SELECT id FROM events WHERE deleted=1)", (now(),))
        # The same open promise twice (stored before promise() caught it): keep one, the owner's when both sides said it
        groups = {}
        for row in db.execute("SELECT p.id,p.who,p.what,p.direction,p.due,p.together,e.occurred_at made_at FROM promises p "
                              "JOIN events e ON e.id=p.event_id WHERE p.status='open' ORDER BY p.id").fetchall():
            groups.setdefault((row['who'].casefold(), ' '.join(row['what'].split()).casefold()), []).append(row)
        for rows in groups.values():
            if len(rows) < 2:
                continue
            keep = next((r for r in rows if r['direction'] == 'mine'), rows[0])
            if len({r['direction'] for r in rows}) > 1 and not (keep['together'] and keep['direction'] == 'mine'):
                db.execute("UPDATE promises SET together=1,direction='mine',check_at=?,updated_at=? WHERE id=?",
                           (promise_check_at('mine', keep['due'], keep['made_at']), now(), keep['id']))
                promise_logged(db, keep['id'], 'together')
            for r in rows:
                if r['id'] != keep['id']:
                    db.execute("UPDATE promises SET status='dropped',note=?,updated_at=? WHERE id=?", (f"The same as promise {keep['id']}", now(), r['id']))
                    promise_logged(db, r['id'], 'merged', keep['id'])
        for row in db.execute("SELECT id,watch FROM promises WHERE status='open' AND watch IS NOT NULL").fetchall():
            watch = {**json.loads(row['watch']), 'promise': True}
            answer = next((e for e in db.execute('SELECT id,account_id,kind,occurred_at,title,metadata FROM events WHERE account_id=? AND kind=? AND occurred_at>? AND deleted=0 ORDER BY occurred_at',
                                                 (watch['account_id'], watch['kind'], watch['since'])) if awaiting_match(watch, dict(e), self.owner_user_ids)), None)
            if answer:
                db.execute("UPDATE promises SET status='answered',note=?,updated_at=? WHERE id=?",
                           (f"They wrote again: {answer['title'][:150]}", now(), row['id']))
                promise_logged(db, row['id'], 'answered', answer['id'])
        # A to-do with a deadline that came to hold someone else's promise after it was made: checked before that deadline
        for row in db.execute("SELECT id,event_id,check_at FROM promises WHERE status='open' AND direction='theirs'").fetchall():
            sooner = before_blocked(db, row['event_id'], row['check_at'], thread=False)
            if sooner != row['check_at']:
                db.execute('UPDATE promises SET check_at=? WHERE id=?', (sooner, row['id']))
        self.close_seen_done(db)
        self.retitle_cut_promises(db)

    def retitle_cut_promises(self, db):
        return retitle_cut_promises(db)

    def promises(self, days=14):
        """Open promises and those closed in the last days, soonest first."""
        since = (dt.datetime.fromisoformat(now()) - dt.timedelta(days=days)).isoformat()
        with self.connect() as db:
            rows = [dict(r) for r in db.execute(
                'SELECT p.id,p.direction,p.who,p.what,p.due,p.check_at,p.status,p.note,p.suggestion_id,p.account_id,p.event_id,p.created_at,p.updated_at,p.together,'
                'e.occurred_at made_at,s.status card_status FROM promises p JOIN events e ON e.id=p.event_id LEFT JOIN suggestions s ON s.id=p.suggestion_id '
                "WHERE p.status IN ('open','carded') OR p.updated_at>=? ORDER BY coalesce(p.due,substr(p.check_at,1,10)),p.id", (since,))]
            for row in rows:
                row['who'] = who_named(db, row['who'])  # one noted before its sender's name was known
                if row['status'] == 'carded':  # the to-do it is now: the one it was merged into, or none when it's gone
                    card = promise_card(db, row['suggestion_id'])
                    row['suggestion_id'], row['card_status'] = (card['id'], card['status']) if card else (None, None)
        for row in rows:
            row['state'] = promise_state(row)
        return [r for r in rows if r['state'] in ('open', 'card') or r['updated_at'] >= since]

    def promise_page(self, promise_id):
        """One promise for its own dashboard page: who promised what to whom and by when, where it stands, the message
        it came from, the people, organization and project that message is on, its card and what happened since."""
        with self.connect() as db:
            row = db.execute('SELECT p.*,e.occurred_at made_at,e.kind source_kind,s.status card_status,s.title card_title FROM promises p '
                             'JOIN events e ON e.id=p.event_id LEFT JOIN suggestions s ON s.id=p.suggestion_id WHERE p.id=?', (promise_id,)).fetchone()
            if not row:
                raise ValueError('Unknown promise')
            p = dict(row)
            p['who'] = who_named(db, p['who'])
            if p['status'] == 'carded':
                card = promise_card(db, p['suggestion_id'])
                p['suggestion_id'], p['card_status'], p['card_title'] = (card['id'], card['status'], card['title']) if card else (None, None, None)
            try:
                links = [dict(r) for r in db.execute("SELECT n.id,n.kind,n.name FROM graph_events g JOIN graph_nodes n ON n.id=g.node_id "
                                                     "WHERE g.event_id=? AND n.kind IN ('person','org','project') ORDER BY n.kind DESC,n.name LIMIT 12", (p['event_id'],))]
            except sqlite3.OperationalError:
                links = []  # no graph yet
            log = [dict(r) for r in db.execute('SELECT at,kind,detail FROM promise_log WHERE promise_id=? ORDER BY at,id', (promise_id,))]
        p['state'] = promise_state(p)
        history = [{'at': p['made_at'], 'kind': 'said', 'detail': p['source_kind']}, {'at': max(p['created_at'], p['made_at']), 'kind': 'noted'}]
        # checked, source and twin: inner steps (a newer message that moved it shows as a source instead)
        history += [h for h in log if h['kind'] not in ('checked', 'source', 'twin') and (h['kind'] != 'together' or h['at'] > p['created_at'])]
        sources = list(dict.fromkeys([int(h['detail']) for h in reversed(log) if h['kind'] == 'source' and str(h['detail']).isdigit()] + [p['event_id']]))
        closed = {'kept': 'kept', 'dropped': 'dropped', 'answered': 'answered'}.get(p['status'])
        if closed and not any(h['kind'] in (closed, 'merged') for h in log):
            history.append({'at': p['updated_at'], 'kind': closed})  # closed before the log
        if p['suggestion_id'] and not any(h['kind'] == 'carded' for h in log):
            history.append({'at': p['updated_at'], 'kind': 'carded'})
        card = {'id': p['suggestion_id'], 'title': p['card_title'], 'status': p['card_status']} if p['suggestion_id'] and p['card_title'] else None
        keep = ('id', 'direction', 'together', 'who', 'what', 'due', 'check_at', 'status', 'state', 'note', 'made_at', 'event_id', 'account_id', 'created_at', 'updated_at')
        return {**{k: p[k] for k in keep}, 'card': card, 'links': links, 'sources': sources, 'history': sorted(history, key=lambda h: h['at'] or '')}

    def promises_text(self, limit=30):
        """Open promises for the review prompt, so a later message can close or move them: those that are a to-do now
        too, so a new date for one moves it instead of making a second promise."""
        lines = []
        for p in [p for p in self.promises() if p['state'] in ('open', 'card')][:limit]:
            made = dt.datetime.fromisoformat(p['made_at']).astimezone(local_tz())
            due = 'due ' + dt.date.fromisoformat(p['due']).strftime('%a, %b ') + str(dt.date.fromisoformat(p['due']).day) if p['due'] else 'no date'
            who = f"you with {p['who']}" if p.get('together') else f"you → {p['who']}" if p['direction'] == 'mine' else f"{p['who']} → you"
            todo = '; a to-do now' if p['state'] == 'card' else ''
            lines.append(f"- #{p['id']} {who}: {p['what']} ({due}; said {made:%a, %b} {made.day}, event {p['event_id']}{todo})")
            memory_use.note('promise', p['id'], lines[-1], 'always', source='signal', at=p['made_at'])
        return '\n'.join(lines)

    def slipped(self, run_id, limit=5):
        """Emails that may have slipped: the owner's own emails that ask something and got no answer in
        4-21 days, and direct questions from people they write with that they haven't answered in 2-14
        days. Each is offered to one review that saves; the review decides if it's worth a card."""
        current = dt.datetime.fromisoformat(now())
        ago = lambda days: (current - dt.timedelta(days=days)).isoformat()
        own = {a['email'].lower() for a in self.accounts if a.get('email') and '@' in a['email']}
        robot = ROBOT_SENDER
        def new_text(body):
            text = (body or '').split('[Quoted earlier messages', 1)[0]
            text = re.split(r'\n(?:On .{5,200} wrote:|Op .{5,200} schreef .{0,40}:|-----Original Message-----)', text, maxsplit=1)[0]
            text = '\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('>'))
            return re.sub(r'(?:https?://|www\.)\S+', '', text)  # a ? in a link (tracking, signatures) isn't a question
        found = {'sent': [], 'asked': []}
        with self.connect() as db:
            done = {r[0] for r in db.execute("SELECT x.event_id FROM slipped x WHERE x.run_id IN (SELECT owner_run FROM analyses WHERE status='complete') OR x.offered_at>?", (ago(0.25),))}
            carded = {r[0] for r in db.execute("SELECT DISTINCT j.value FROM suggestions s, json_each(s.event_ids) j")}
            followed = follow_ups.covered(db)  # the owner's own emails there: automated follow-ups look after them (follow_ups.py)
            later = ("SELECT 1 FROM events r WHERE r.account_id=e.account_id AND r.kind='gmail.message' AND r.deleted=0 AND r.occurred_at>e.occurred_at "
                     "AND json_extract(r.metadata,'$.thread_id')=json_extract(e.metadata,'$.thread_id')")
            rows = db.execute("SELECT e.id,e.account_id,e.occurred_at,e.title,e.body,e.metadata, instr(e.metadata,'\"SENT\"')>0 mine FROM events e "
                              "WHERE e.kind='gmail.message' AND e.deleted=0 AND e.history=0 AND e.occurred_at>? AND e.occurred_at<? "
                              f"AND ((instr(e.metadata,'\"SENT\"')>0 AND e.occurred_at<? AND NOT EXISTS ({later})) "
                              f"OR (instr(e.metadata,'\"SENT\"')=0 AND e.occurred_at>? AND NOT EXISTS ({later} AND instr(r.metadata,'\"SENT\"')>0))) "
                              "ORDER BY e.occurred_at", (ago(21), ago(2), ago(4), ago(14))).fetchall()
            for row in rows:
                if row['id'] in done or row['id'] in carded or (row['mine'] and row['id'] in followed) or '?' not in new_text(row['body']):
                    continue
                m = json.loads(row['metadata'])
                if 'SENT' not in m.get('labels', []) and not row['mine']:
                    sender = _address(m.get('from'))
                    to = [x.lower() for x in re.findall(r'[^\s<>"\',;]+@[^\s<>"\',;]+', m.get('to') or '')]
                    automated = AUTOMATED_LABELS & set(m.get('labels', []))
                    if not sender or sender in own or robot.match(sender) or automated or not own & set(to) or len(to) > 2:
                        continue
                    # Only people the owner writes with: no cold pitches or newsletters.
                    if not db.execute("SELECT 1 FROM events WHERE kind='gmail.message' AND instr(metadata,'\"SENT\"')>0 AND instr(lower(json_extract(metadata,'$.to')),?)>0 LIMIT 1", (sender,)).fetchone():
                        continue
                    found['asked'].append((row, sender))
                elif row['mine']:
                    to = [x.lower() for x in re.findall(r'[^\s<>"\',;]+@[^\s<>"\',;]+', m.get('to') or '')]
                    people = [x for x in to if x not in own and not robot.match(x)]
                    # Not outreach: in a thread the other person started, or to someone who had
                    # written to the owner before the owner started this thread.
                    first = db.execute("SELECT occurred_at,instr(metadata,'\"SENT\"')>0 mine FROM events WHERE account_id=? AND kind='gmail.message' "
                                       "AND json_extract(metadata,'$.thread_id')=? ORDER BY occurred_at LIMIT 1", (row['account_id'], m.get('thread_id'))).fetchone()
                    if first and first['mine']:
                        people = [x for x in people if db.execute("SELECT 1 FROM events WHERE kind='gmail.message' AND occurred_at<? AND instr(metadata,'\"SENT\"')=0 "
                                                                  "AND instr(lower(json_extract(metadata,'$.from')),?)>0 LIMIT 1", (first['occurred_at'], x)).fetchone()]
                    if people:
                        found['sent'].append((row, ', '.join(people[:3])))
            day = lambda row: dt.datetime.fromisoformat(row['occurred_at']).astimezone(local_tz()).strftime('%a, %b %-d')
            waited = lambda row: (current - dt.datetime.fromisoformat(row['occurred_at'])).days
            # Three or more emails sent the same day with the same subject pattern are outreach: left out.
            batches = {}
            for row, who in found['sent']:
                shape = ' '.join(re.sub(r'(?i)^(?:(?:re|fwd?|aw|wg|tr)\s*:\s*)+', '', row['title'] or '').lower().split()[:2])
                batches.setdefault((row['account_id'], day(row), shape), []).append((row, who))
            items = [([r], f"- No answer for {waited(r)} days: the owner emailed {who_} \"{r['title'][:120]}\" on {when} ({account}, event {r['id']}).")
                     for (account, when, _), group in batches.items() if len(group) < 3 for r, who_ in group]
            items = items[-limit:] + [([r], f"- Waiting {waited(r)} days on the owner: {who} asked \"{r['title'][:120]}\" on {day(r)} ({r['account_id']}, event {r['id']}).")
                                      for r, who in found['asked'][-limit:]]
            for rows_, _ in items:
                for row in rows_:
                    db.execute('INSERT INTO slipped(event_id,kind,run_id,offered_at) VALUES(?,?,?,?) ON CONFLICT(event_id) DO UPDATE SET run_id=excluded.run_id,offered_at=excluded.offered_at',
                               (row['id'], 'sent' if row['mine'] else 'asked', run_id, now()))
        return '\n'.join(line for _, line in items)
