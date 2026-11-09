"""Who is on a thread, for the Shared Graph's rules (shared_graph.Scope, docs/shared-graph.md): the thread and the
conversation a message is part of, the addresses on it, which threads are only automated mail, and which have someone
kept private on any of their messages. Keep private and Only you hold for the whole conversation, so both are asked
per thread, from all its messages (history too), in one read of the accounts' messages per scope."""
import collections
import json
import re

import graph

ADDRESS = re.compile(r'[^@\s<>",;]+@[^@\s<>",;]+\.[^@\s<>",;]+')
MAIL_KINDS = ('gmail.message', 'ms_graph.message', 'outlook.message', 'salesflare.email', 'intercom.conversation')
# A project's timeline beyond its email threads: meetings and their notes, Intercom conversations and chats. On a board
# the team sees, or one shared with chosen teammates, they count as shared by being on it (visibility).
ITEM_KINDS = ('calendar.event', 'salesflare.meeting', 'zoom.summary', 'meeting.notes', 'meeting.transcript', 'intercom.conversation', 'whatsapp.message', 'slack.message', 'teams.message',
              'linkedin.message', 'x.dm', 'x.mention', 'telegram.message', *graph.DOC_KINDS)
MAIL, ITEMS = frozenset(MAIL_KINDS), frozenset(ITEM_KINDS)
NEEDLES = 64  # at most this many private addresses and domains are looked for by name in SQL; more: every row with an address
PLAIN = re.compile(r'[ !#-.0-\[\]-~]+')  # an address JSON text holds as it is: ASCII, no quote, slash or backslash
# The domain of every address in a message's metadata as stored (JSON text, lowercased): what follows an @ up to where
# ADDRESS stops. ESCAPED: text that may hold one in another form (an escaped ASCII character, a Kelvin sign).
FEW = 8  # up to this many private domains are looked for one by one, which is faster than finding every domain
DOMAIN = re.compile(r'@([^@\s<>",;\\]+)')
ESCAPED = re.compile(r'\\u(?:00[0-7]|212[aA])')


def thread_of(kind, metadata, event_id):
    key, _ = graph.thread_key(kind, metadata or {})
    return key or f'ev:{event_id}'


def conversation_of(kind, metadata):
    """The ongoing conversation a message is part of, where that is more than its thread: a Slack direct message (each
    of its messages is its own thread) and a Teams one-on-one chat or channel thread (a Teams message has no thread
    key). None for the rest: a mail thread or a WhatsApp chat is one thread already. Only ever read to keep more with
    the owner (Only you on it, or someone kept private in it), never to share more."""
    metadata = metadata or {}
    if kind == 'slack.message' and metadata.get('conversation_type') == 'dm' and metadata.get('channel_id'):
        return 'sl:' + str(metadata['channel_id'])
    if kind == 'teams.message' and metadata.get('chat_id') and metadata.get('chat_kind') in ('oneOnOne', 'channel'):
        return 'teams:' + str(metadata['chat_id'])
    return None


def unit_of(kind, metadata, event_id):
    """What Only you and Keep private hold for as a whole: the conversation, else the thread."""
    return conversation_of(kind, metadata) or thread_of(kind, metadata, event_id)


def _kept_conversations(db):
    """The conversations (conversation_of) the owner chose Only you in: what arrives in them afterwards stays too."""
    found = set()
    for kind, key in db.execute(
            "SELECT DISTINCT e.kind, CASE e.kind WHEN 'slack.message' THEN json_extract(e.metadata,'$.channel_id') "
            "ELSE json_extract(e.metadata,'$.chat_id') END FROM share_threads s JOIN events e ON e.id=s.event_id "
            "WHERE s.hand='private' AND e.deleted=0 AND ((e.kind='slack.message' AND json_extract(e.metadata,'$.conversation_type')='dm') "
            "OR (e.kind='teams.message' AND json_extract(e.metadata,'$.chat_kind') IN ('oneOnOne','channel')))"):
        if key:
            found.add(('sl:' if kind == 'slack.message' else 'teams:') + str(key))
    return found


def addresses(metadata):
    found = []
    for field in ('from', 'to', 'cc'):
        value = metadata.get(field)
        for part in value if isinstance(value, list) else [value]:
            found += [a.lower() for a in ADDRESS.findall(str(part or ''))]
    return found


AUTOMATED_LABELS = graph.BULK_LABELS | {'SPAM'}  # what Gmail (and ms_graph's mapping) files as not a person writing


def item_people(metadata):
    """Everyone on a meeting, its notes or a chat, besides addresses(): the organizer and invitees, the host, the contact."""
    found = addresses(metadata)
    for a in [metadata.get('organizer'), *(metadata.get('attendees') or [])]:
        if isinstance(a, dict) and '@' in str(a.get('email') or ''):
            found.append(str(a['email']).strip().lower())
    for field in ('host_email', 'contact_email'):
        if '@' in str(metadata.get(field) or ''):
            found.append(str(metadata[field]).strip().lower())
    return found


def automated_message(metadata):
    """A message no person wrote to the owner: from a system sender (graph.bulk: no-reply, notifications, receipts,
    invoices, billing; graph.relay) or filed by the mailbox as an update, promotion, social, forum or spam message."""
    if AUTOMATED_LABELS & set(metadata.get('labels') or ()):
        return True
    sender = ADDRESS.findall(str(metadata.get('from') or ''))
    return bool(sender) and (graph.bulk(sender[0].lower()) or graph.relay(sender[0].lower()))


class Kept:
    """What a Scope reads from the messages themselves: mixed into shared_graph.Scope."""

    def hand(self, thread, kind, metadata):
        """The owner's choice for a thread: its own, else Only you when they chose that for the conversation it is in
        (kept_conversations), so a message that arrives there later stays with them too."""
        hand = (self.calls.get(thread) or (None, None))[1]
        if hand is None and self.kept_conversations and conversation_of(kind, metadata) in self.kept_conversations:
            return 'private'
        return hand

    def _field_private(self, value, memo):
        """Whether a from, to or cc value (as addresses reads it) has someone kept private on it. memo: by its text,
        since most messages repeat a few."""
        for part in value if isinstance(value, list) else (value,):
            text = str(part or '')
            hit = memo.get(text)
            if hit is None:
                hit = memo[text] = any(self.private_address(a.lower()) for a in ADDRESS.findall(text))
            if hit:
                return True
        return False

    def _mark(self, e, metadata, found, memo):
        """Adds this message's unit (unit_of) to found (by address, by an item's people, by link) when someone kept
        private is on it, read the way visibility reads one message."""
        kind = e['kind']
        tied = e['id'] in self.private_events
        hit = any(self._field_private(metadata.get(f), memo) for f in ('from', 'to', 'cc')) or (
            kind == 'slack.message' and any(self.private_address(a) for a in self.slack_people(metadata)))
        on_item = hit or (kind in ITEMS and any(self.private_address(a) for a in item_people(metadata)))
        if not (tied or on_item):
            return
        unit = unit_of(kind, metadata, e['id'])
        plain, items, linked = found
        if tied:
            linked.add(unit)
        if hit:
            plain.add(unit)
        if on_item:
            items.add(unit)

    def _private_marks(self, rows, found):
        memo = {}
        for e in rows:
            self._mark(e, json.loads(e['metadata'] or '{}'), found, memo)
        return found

    def _anyone_private(self):
        return bool(self.accounts and (self.private_ids or self.private_events))

    def _candidates(self):
        """(SQL, arguments): the messages someone kept private can be on, found by SQLite so only those are read and
        checked (_mark keeps the exact ones; the same answer as checking every message, _private_full). The ones
        linked to them; a Slack message with their member id in it; and any message whose metadata has one of their
        addresses or domains in it. With many of those (NEEDLES), or one JSON may hold in another form, any message
        with an address at all (any Slack message, for many member ids). One with an escaped character or a Kelvin
        sign (it lowercases to k) is always read: its text is not what SQL sees."""
        parts, args = ['id IN (SELECT value FROM json_each(?))', 'instr(metadata,?)>0', 'instr(metadata,?)>0'], [
            json.dumps(sorted(self.private_events)), '\\u', '\u212a']
        members = sorted(u for u, mail in self.slack_email.items() if self.private_address(mail))
        if len(members) > NEEDLES:
            parts.append("kind='slack.message'")
        elif members:
            parts.append("(kind='slack.message' AND (" + ' OR '.join(['instr(metadata,?)>0'] * len(members)) + '))')
            args += members
        needles = sorted(self.private_ids)
        if len(needles) <= NEEDLES and all(PLAIN.fullmatch(n) for n in needles):
            parts += ['metadata LIKE ?'] * len(needles)  # ASCII, any case; _ and % only find more
            args += ['%' + n + '%' for n in needles]
        else:
            parts.append("instr(metadata,'@')>0")
        return '(' + ' OR '.join(parts) + ')', args

    def _domains(self):
        """The domains of everyone kept private, to tell from a message's stored metadata that none of them is on it
        (_maybe): as '@domain' texts to look for when they are few, else as a set. None when one of them can't be
        looked for that way: every message is checked then."""
        found = {n.rsplit('@', 1)[-1] for n in self.private_ids if '@' in n}
        if not all(d.isascii() and DOMAIN.fullmatch('@' + d) for d in found):
            return None
        return tuple('@' + d for d in sorted(found)) if len(found) <= FEW else found

    @staticmethod
    def _maybe(raw, domains):
        """Whether someone at one of these domains can be on a message, from its metadata as stored: no JSON read, no
        address parsed for the many they are not on. Never no for one they are on (_mark decides)."""
        if domains is None or ('\\u' in raw and ESCAPED.search(raw)):
            return True
        low = raw.lower()
        if isinstance(domains, tuple):
            for text in domains:
                if text in low:
                    return True
            return False
        return not domains.isdisjoint(DOMAIN.findall(low))

    def _in_accounts(self, accounts):
        """The SQL for "in these accounts" (a JSON list, the next argument). When they hold a good part of all messages,
        as the accounts a Machine shares do, reading the table through is a few times faster than going account by
        account through the index: the + keeps SQLite off it. The same rows either way."""
        most = self._db.execute('SELECT (SELECT count(*) FROM events WHERE account_id IN (SELECT value FROM json_each(?)))*4 >= (SELECT count(*) FROM events)',
                                (accounts,)).fetchone()[0]
        return ('+' if most else '') + 'account_id IN (SELECT value FROM json_each(?))'

    def _read(self):
        """automated and private_units in one read of the accounts' messages (whichever is still asked for): all mail
        for the first, as before; for the second, of the rest only the messages someone kept private can be on
        (_candidates), and each is checked only when its stored metadata has one of their domains (_maybe). A year of
        history is most of what a Machine holds, and collect reads only the signals, so a second read of everything
        doubled a share round."""
        units = self._private_found.get('units')
        auto, private = self._automated is None, units is None and self._anyone_private()
        found, spoken, marks, memo = set(), set(), (set(), set(), set()), {}
        if self.accounts and (auto or private):
            wanted, args = [], [json.dumps(sorted(self.accounts))]
            if auto:
                wanted.append('kind IN (SELECT value FROM json_each(?))')
                args.append(json.dumps(sorted(MAIL_KINDS)))
            if private:
                sql, more = self._candidates()
                wanted.append(sql)
                args += more
                domains, linked = self._domains(), self.private_events
            for e in self._db.execute('SELECT id,kind,metadata FROM events WHERE deleted=0 AND ' + self._in_accounts(args[0]) +
                                      ' AND (' + ' OR '.join(wanted) + ')', args):
                kind, raw = e['kind'], e['metadata'] or '{}'
                mail = auto and kind in MAIL
                maybe = private and (e['id'] in linked or kind == 'slack.message' or self._maybe(raw, domains))
                if not (mail or maybe):
                    continue
                metadata = json.loads(raw)
                if mail:
                    thread = thread_of(kind, metadata, e['id'])
                    if thread not in spoken:
                        if self.owner_side(metadata) or not automated_message(metadata):
                            spoken.add(thread)
                            found.discard(thread)
                        else:
                            found.add(thread)
                if maybe:
                    self._mark(e, metadata, marks, memo)
        if auto:
            self._automated = found
        if units is None:
            self._private_found['units'] = marks

    def _private_full(self):
        """private_units by checking every message: what _read's narrower one must equal (tests, measurements)."""
        found = (set(), set(), set())
        if self._anyone_private():
            self._private_marks(self._db.execute('SELECT id,kind,metadata FROM events WHERE deleted=0 AND account_id IN (SELECT value FROM json_each(?))',
                                                 (json.dumps(sorted(self.accounts)),)), found)
        return found

    @property
    def private_units(self):
        """(by address, by an item's people, by link): the threads and conversations (unit_of) with someone kept private
        on any of their messages, history too. Keep private is for the whole thread: a later reply without them stays
        with the owner too. Worked out once per scope (_read), not once per message; nothing is read when nobody is
        private."""
        if self._private_found.get('units') is None:
            self._read()
        return self._private_found['units']

    def private_among(self, units, accounts=()):
        """private_units for just these units, from their own messages (a unit's answer depends only on those), so a
        page reads its own threads and not every message. accounts: where the chats and channels among them are. The
        scope then answers for these units only, so it is for a scope made for one call (thread_labels, held_back)."""
        memo = self._private_memo
        asked = {u for u in units if u}
        wanted = asked - set(memo) if memo is not None else asked
        found = (set(), set(), set())
        if wanted and self.accounts and (self.private_ids or self.private_events):
            self._private_marks(self._unit_rows(wanted, accounts), found)
        if memo is not None:
            memo.update((u, tuple(u in part for part in found)) for u in wanted)
            found = tuple({u for u in asked if (memo.get(u) or (0, 0, 0))[i]} for i in range(3))
        self._private_found['units'] = found
        return found

    def _unit_rows(self, wanted, accounts=()):
        """Every message whose unit can be one of these, by the plain keys graph.thread_key and conversation_of read (a
        superset: _private_marks keeps the exact ones). Mail and Intercom by their own index; a recurring meeting by the
        calendar's; a chat or channel by a pass over the accounts it is in only. A message that is its own thread
        (ev:) is read by visibility itself."""
        rest = collections.defaultdict(set)
        for unit in wanted:
            prefix, _, value = unit.partition(':')
            if unit.startswith(('linkedin.message:', 'x.dm:')):
                prefix, value = 'conversation', unit.split(':', 1)[1]
            rest[{'gm': 'thread', 'sf': 'thread', 'ic': 'conversation', 'xc': 'conversation', 'sl': 'channel', 'wa': 'chat', 'tg': 'chat',
                  'teams': 'chat', 'cal': 'meeting'}.get(prefix, prefix)].add(value.split(':')[0] if prefix == 'sl' else value)
        # a key is asked as text and as a number, as json_extract gives either
        both = lambda name: json.dumps(sorted({v for x in rest.get(name, ()) for v in ((x, int(x)) if x.isdigit() else (x,))}, key=str))
        mine = json.dumps(sorted(self.accounts))
        ids = set()
        if rest.get('thread'):
            ids |= {r[0] for r in self._db.execute("SELECT id FROM events WHERE json_extract(metadata,'$.thread_id') IN (SELECT value FROM json_each(?)) "
                                                   "AND +kind IN ('gmail.message','salesflare.email')", (both('thread'),))}
        if rest.get('conversation'):
            ids |= {r[0] for r in self._db.execute("SELECT id FROM events WHERE json_extract(metadata,'$.conversation_id') IN (SELECT value FROM json_each(?))",
                                                   (both('conversation'),))}
        if rest.get('meeting'):
            ids |= {r[0] for r in self._db.execute("SELECT id FROM events WHERE kind='calendar.event' AND json_extract(metadata,'$.recurring_event_id') "
                                                   'IN (SELECT value FROM json_each(?))', (both('meeting'),))}
        if rest.get('channel') or rest.get('chat'):
            where = json.dumps(sorted(set(accounts) & self.accounts or self.accounts))
            # no index by channel or chat: of the accounts' messages, only those someone kept private can be on are opened
            sql, args = self._candidates()
            ids |= {r[0] for r in self._db.execute(
                'SELECT id FROM events WHERE ' + self._in_accounts(where) + " AND kind IN ('slack.message','whatsapp.message','telegram.message','teams.message') "
                'AND ' + sql + " AND ((kind='slack.message' AND json_extract(metadata,'$.channel_id') IN (SELECT value FROM json_each(?))) OR "
                "(kind<>'slack.message' AND json_extract(metadata,'$.chat_id') IN (SELECT value FROM json_each(?))))", (where, *args, both('channel'), both('chat')))}
        if not ids:
            return []
        return self._db.execute('SELECT id,kind,metadata FROM events WHERE deleted=0 AND account_id IN (SELECT value FROM json_each(?)) '
                                'AND id IN (SELECT value FROM json_each(?))', (mine, json.dumps(sorted(ids)))).fetchall()

    def private_on(self, unit, item=False):
        """Whether someone kept private is on any message of this thread or conversation (item: read as a board's
        meeting or chat, with its organizer, invitees, host and contact)."""
        return unit in self.private_units[1 if item else 0]

    def private_linked(self, unit):
        """Whether a message of this thread or conversation is linked to someone of the owner's own life."""
        return unit in self.private_units[2]

    @property
    def automated(self):
        """Threads that are only automated mail: nobody on the owner's side wrote in them, and every message in them comes
        from a system sender (no-reply, notifications, receipts, billing, relays) or is one the mailbox itself filed as
        an update, promotion, social, forum or spam message. Never a client conversation, whatever the review said: their
        receipts, invoices, alerts and newsletters never go (automated_message)."""
        if self._automated is None:
            self._read()
        return self._automated

    def automated_only(self, threads):
        """`automated` for just these threads, from their own messages: a thread's answer depends only on its own
        messages, so it is the same as the full set's for them. Reading every mail message (and opening each sealed
        one) took seconds on each person's page; this reads a page's threads only. The scope then answers for these
        threads only, so it is for a scope made for one call (thread_labels)."""
        memo = getattr(self, '_automated_memo', None)
        asked = {t for t in threads if t}
        wanted = asked - set(memo) if memo is not None else asked  # a page asks twice (timeline, labels): once each
        found = set()
        if self.accounts and wanted:
            ids = [t[3:] for t in wanted if t.startswith('ev:') and t[3:].isdigit()]
            # every message whose thread can be one of these, by the plain keys graph.thread_key reads (a superset:
            # thread_of below keeps the exact ones)
            spoken, seen = set(), set()
            # each part by its own index (events_thread_id, events_conversation: Store; +kind keeps SQLite off the kind
            # index), never a pass over all mail;
            # a key is asked as text and as a number, as json_extract gives either
            keyed_as = lambda prefixes: json.dumps(sorted({v for t in wanted if t.startswith(prefixes)
                                                           for v in ((t[3:], int(t[3:])) if t[3:].isdigit() else (t[3:],))}, key=str))
            for e in self._db.execute(
                    'SELECT id,kind,metadata FROM events WHERE deleted=0 AND kind IN (SELECT value FROM json_each(?)) '
                    'AND account_id IN (SELECT value FROM json_each(?)) AND id IN ('
                    "SELECT id FROM events WHERE json_extract(metadata,'$.thread_id') IN (SELECT value FROM json_each(?)) "
                    "AND +kind IN ('gmail.message','salesflare.email') UNION "
                    "SELECT id FROM events WHERE json_extract(metadata,'$.conversation_id') IN (SELECT value FROM json_each(?)) "
                    "AND +kind='intercom.conversation' UNION "
                    'SELECT value FROM json_each(?))',
                    (json.dumps(sorted(MAIL_KINDS)), json.dumps(sorted(self.accounts)), keyed_as(('gm:', 'sf:')), keyed_as(('ic:',)),
                     json.dumps([int(i) for i in ids]))):
                metadata = json.loads(e['metadata'] or '{}')
                thread = thread_of(e['kind'], metadata, e['id'])
                if thread not in wanted:
                    continue
                seen.add(thread)
                if self.owner_side(metadata) or not automated_message(metadata):
                    spoken.add(thread)
            found = seen - spoken
        if memo is not None:
            memo.update((t, t in found) for t in wanted)
            found = {t for t in asked if memo.get(t)}
        self._automated = found
        return found
