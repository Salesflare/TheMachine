"""One person in a chat and at an address: what a one-to-one chat (LinkedIn, WhatsApp, Telegram, Signal, X) shows about
an address with the same first name (docs/intelligence.md, Same person?). Plain code over this Machine's own signals,
worked out again each build; nothing is stored, no link is opened and no model is asked.

Two things a chat shows:
- an address written in it. By them: it is theirs. By the owner: a question.
- a meeting made out of it: the owner sent a booking link there (a link the app knows, or any link when the meeting itself
  carries a booking tool's mark: a short link that redirects reads as any other), or the two wrote back and forth, and
  soon after a meeting with that address as its only guest from outside was made.

The same first name right after a link is not enough to join by itself: on a busy Machine somebody else with that first
name does book in the same days now and then. Their company named in the chat (or their LinkedIn headline), or the
surname in the address or on the booking, makes that next to impossible. So with one of those, and nobody else it could
be, they are one person (with why and Undo on their page). Without, it is a question; a meeting with no link before it is
a question only with one of those, and nothing without."""
import collections
import datetime as dt
import json
import re

from graph import DOMAIN_PREFIXES, DOMAIN_SUFFIXES, folded_words, name_match, name_words, parse_time
from mail_senders import address_name, bulk
from whatsapp_images import MARK
import enrichment

ASKS = {'written': 'This address is in your chat', 'meeting': 'A meeting made from their chat'}  # why a question is asked
SPACES = ('li', 'wa', 'tg', 'sig', 'x')
SURE = dt.timedelta(days=7)   # from the owner's link to the meeting, when something besides the first name agrees
ASK = dt.timedelta(hours=72)  # ... when nothing does, and from a message both ways when there was no link
LINK = re.compile(r'https?://[^\s<>"\'\])]+', re.I)
ADDRESS = re.compile(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+')
# Where booking pages live. A link there is a booking link, and a meeting whose text has one was booked on such a page.
BOOKING = re.compile(
    r'https?://(?:[\w-]+\.)*(?:calendly\.com|cal\.com|cal\.eu|savvycal\.com|youcanbook\.me|tidycal\.com|zcal\.co|koalendar\.com|'
    r'acuityscheduling\.com|as\.me|chilipiper\.com|oncehub\.com|scheduleonce\.com|appointlet\.com|vyte\.in|lemcal\.com|setmore\.com|'
    r'simplybook\.(?:me|it)|zohobookings\.(?:com|eu|in)|usemotion\.com/meet|book\.vimcal\.com|calendar\.app\.google|scheduler\.zoom\.us|'
    r'meetings(?:-\w+)?\.hubspot\.com|app\.reclaim\.ai/m|calendar\.notion\.so/meet|doodle\.com/bp|bookings\.cloud\.microsoft|'
    r'calendar\.google\.com/calendar/(?:u/\d+/)?appointments|outlook\.(?:office|office365|live)\.com/(?:bookwithme|book|owa/calendar/[^\s/]+/bookings))'
    r'(?=[/?#:\s]|$)', re.I)


def find(db, per_event, union, keys, best, booking_links=()):
    """([(chat identity, address identity, 'written' or 'booking')] to join, {(chat identity, address identity): why}
    to ask), for pairs that are not one person yet."""
    proof = _Proof(db, per_event, union, keys, best, booking_links)
    return proof.found() if proof.fitting else ([], {})


def local_words(address):
    return [w for w in re.split(r'[^a-z]+', address.lower().partition('@')[0].partition('+')[0]) if w]


class _Proof:
    def __init__(self, db, per_event, union, keys, best, booking_links):
        self.db, self.per_event, self.union, self.keys, self.best = db, per_event, union, keys, best
        self.links = tuple(re.sub(r'(?i)^https?://(www\.)?', '', str(u)).rstrip('/').casefold() for u in booking_links or () if u)
        self.chats = collections.defaultdict(list)   # a person's own chat -> [(at, event, the owner wrote it)]
        self.headlines = {}
        seen = set()
        for event_id, (_, at, _, m, found) in per_event.items():
            seen |= {i for i, *_ in found}
            identifier, _, _, role = found[0]
            if role in ('owner', 'them') and identifier.split(':', 1)[0] in SPACES:
                self.chats[identifier].append((at, event_id, role == 'owner'))
                if isinstance(m.get('headline'), str) and m['headline'].strip():
                    self.headlines[identifier] = m['headline']
        named = {c: w for c in self.chats if (w := name_words(best(c), c)) and len(w[0]) >= 2 and ' '.join(w) not in keys.owner.names}
        self.names = {i: w for i in seen if (w := name_words(best(i), i) if best(i) else [])}
        self.firsts = {w[0] for w in (*named.values(), *self.names.values())}
        self.chat_words = named
        by_first = collections.defaultdict(list)
        for c, w in named.items():
            by_first[w[0]].append(c)
        # address -> [(chat, whether the surname agrees too)]: the same first name and no other surname
        self.fitting = collections.defaultdict(list)
        for i in seen:
            if not i.startswith('email:') or keys.owner.has(i) or i.rsplit('@', 1)[-1] in keys.owner.domains or keys.shared(i):
                continue
            for c in {c for w in self._firsts_of(i) for c in by_first.get(w, ())}:
                if union.find(c) != union.find(i) and (fits := self._fits(named[c], i)) and not self._other_chat(c, i):
                    self.fitting[i].append((c, fits == 'full'))
        self._known_orgs = None

    def _firsts_of(self, identifier):
        words, local = self.names.get(identifier), local_words(identifier[6:])
        return {words[0]} if words else {f for f in self.firsts if local and local[0].startswith(f)} if local else set()

    def _fits(self, chat, identifier):
        """'full' (the surname agrees too), 'first' or None (another name, or the address has another surname)."""
        words, local = self.names.get(identifier), local_words(identifier[6:])
        first, surname, joined = chat[0], chat[-1] if len(chat) >= 2 and len(chat[-1]) >= 2 else '', ''.join(local)
        if words:
            if words[0] != first or not name_match(chat, words):
                return None
            if surname and len(words) >= 2 and words[-1] == surname:
                return 'full'
            other = address_name(identifier[6:], self.firsts).split()
            if other and other[0].casefold() != first:
                return None  # a colleague's address, under their name
        if surname and (joined in (first + surname, surname + first) or (words or local[:1] == [first]) and surname in local):
            return 'full'
        if joined.startswith(first) and (tail := joined[len(first):]):
            if not words and local[0] != first or surname and not surname.startswith(tail):
                return None  # anna@ is not Ann, sam.wu@ and samwu@ are not Sam Lee
        label = enrichment.registrable(identifier.rsplit('@', 1)[-1]).split('.')[0]
        return 'full' if len(surname) >= 4 and surname in label else 'first'

    def _other_chat(self, chat, identifier):
        """The address' person already has another chat on the same service: theirs is known."""
        space = chat.split(':', 1)[0] + ':'
        return any(i.startswith(space) and i != chat for i in self.union.members[self.union.find(identifier)])

    def found(self):
        sure, ask = self._written_in_chats()
        for chat, identifier, join in self._meetings():
            if join and (chat, identifier) not in sure:
                sure[(chat, identifier)] = 'booking'
            elif not join:
                ask.setdefault((chat, identifier), ASKS['meeting'])
        return [(c, i, why) for (c, i), why in sorted(sure.items())], {pair: why for pair, why in sorted(ask.items()) if pair not in sure}

    # An address written in a chat

    def _written_in_chats(self):
        chats = {c for fits in self.fitting.values() for c, _ in fits}
        wrote = {e: (c, mine) for c in chats for _, e, mine in self.chats[c]}
        by_address = collections.defaultdict(lambda: ([], []))  # address -> (chats they wrote it in, chats the owner did)
        for event_id, found in self._addresses_in(wrote).items():
            c, mine = wrote[event_id]
            for address in found:
                by_address['email:' + address][int(mine)].append(c)
        sure, ask = {}, {}
        for identifier, fits in self.fitting.items():
            theirs, owners = by_address.get(identifier, ((), ()))
            if len({self.union.find(c) for c in (*theirs, *owners)}) != 1:
                continue  # in nobody's chat, or passed around in several: whose it is stays open
            one = len({self.union.find(c) for c, _ in fits}) == 1
            for c, full in fits:
                if c in theirs and (full or one):
                    sure[(c, identifier)] = 'written'
                elif c in theirs or c in owners:
                    ask[(c, identifier)] = ASKS['written']
        return sure, ask

    def _addresses_in(self, events):
        return {e: {a.lower().strip('.-') for a in ADDRESS.findall(body.partition(MARK)[0])}  # not what was read off a picture
                for e, body in self._bodies(sorted(events)).items() if '@' in body}

    def _bodies(self, ids):
        out = {}
        for start in range(0, len(ids), 500):
            chunk = ids[start:start + 500]
            out.update({r[0]: str(r[1] or '') for r in self.db.execute(f"SELECT id,body FROM events WHERE id IN ({','.join('?' * len(chunk))})", chunk)})
        return out

    # A meeting made from a chat

    def _made(self):
        """[(address identity, event, when the meeting was made)] of the owner's meetings with one guest from outside
        and no series. When: the calendar's own time of making it, else the first mail with that address when the
        meeting was last changed no earlier than that (a booking page mails its confirmation)."""
        mail, meetings = {}, []
        for event_id, (kind, at, _, m, found) in self.per_event.items():
            if kind == 'gmail.message':
                for i, *_ in found:
                    if i in self.fitting and (i not in mail or at < mail[i]):
                        mail[i] = at
            elif kind == 'calendar.event' and not m.get('recurring_event_id'):
                guests = [i for i, _, _, role in found if role == 'met' and i.rsplit('@', 1)[-1] not in self.keys.owner.domains]
                if len(guests) == 1 and guests[0] in self.fitting:
                    meetings.append((guests[0], event_id, m))
        out = []
        for identifier, event_id, m in meetings:
            try:
                made = parse_time(m['created']) if m.get('created') else None
                if made is None and m.get('updated') and identifier in mail:
                    made = min(mail[identifier], parse_time(m['updated']))
            except (TypeError, ValueError):
                made = None
            if made:
                out.append((identifier, event_id, made))
        return out

    def _meetings(self):
        """(chat, address, whether it is enough to join them)."""
        hits = []
        for identifier, meeting, made in self._made():
            for c, full in self.fitting[identifier]:
                near = [(at, e, mine) for at, e, mine in self.chats[c] if dt.timedelta(0) <= made - at <= SURE]
                if near:
                    hits.append((c, identifier, meeting, made, full, near))
        if not hits:
            return
        bodies = self._bodies(sorted({e for *_, near in hits for _, e, mine in near if mine} | {h[2] for h in hits}))
        pairs = collections.defaultdict(list)
        for c, identifier, meeting, made, full, near in hits:
            booked = bool(BOOKING.search(bodies.get(meeting, '')))
            linked = max((at for at, e, mine in near if mine and self._booking_link(bodies.get(e, ''), booked)), default=None)
            close = [mine for at, _, mine in near if made - at <= ASK]
            if linked or len(set(close)) == 2:
                pairs[(c, identifier)].append((linked, made, full))
        booked_for = collections.defaultdict(set)  # whose link, as a person -> the addresses that came out of it
        for (c, identifier), found in pairs.items():
            booked_for[self.union.find(c)].add(self.union.find(identifier))
        for (c, identifier), found in sorted(pairs.items()):
            linked, made, full = max(found, key=lambda f: (bool(f[0]), f[1]))
            agrees = full or self._company(c, identifier, made)
            alone = len(booked_for[self.union.find(c)]) == 1 and not self._rivals(c, identifier, made)
            if not agrees and not (linked and alone and made - linked <= ASK):
                continue  # a first name and a busy week: nothing to ask
            if not linked and not alone:
                continue
            yield c, identifier, bool(agrees and linked and alone and not self._works_elsewhere(c, identifier))

    def _booking_link(self, text, booked):
        for link in LINK.findall(text):
            if booked or BOOKING.match(link):
                return True
            plain = re.sub(r'(?i)^https?://(www\.)?', '', link).rstrip('/.,!').casefold()
            if any(plain == known or plain.startswith((known + '/', known + '?', known + '#')) for known in self.links):
                return True
        return False

    def _company(self, chat, identifier, made):
        """Whether the address' company is named in that chat up to then, in their headline, or as where they work."""
        domain = identifier.rsplit('@', 1)[-1]
        label = re.sub(r'[^a-z0-9]', '', enrichment.registrable(domain).split('.')[0])
        if domain in self.keys.freemail or len(label) < 3 or label == self.chat_words[chat][0] or bulk(identifier[6:]):
            return False
        names = {label} | {label[len(p):] for p in DOMAIN_PREFIXES if label.startswith(p)} | {label[:-len(s)] for s in DOMAIN_SUFFIXES if label.endswith(s)}
        names = {n for n in names if n == label or len(n) >= 5}
        if self._known_orgs is None:
            self._known_orgs = collections.defaultdict(set)
            for r in self.db.execute('SELECT identifier,org,org_id FROM person_orgs'):
                self._known_orgs[r[0]] |= {str(r[1] or ''), str(r[2] or '').removeprefix('org:').split('.')[0]}
        texts = [self.headlines.get(chat, ''), *self._known_orgs.get(chat, ()),
                 *self._bodies([e for at, e, _ in self.chats[chat] if at <= made]).values()]
        return any(_names(text, names) for text in texts if text)

    def _works_elsewhere(self, chat, identifier):
        """The chat's person is already known at another company's address."""
        domain = identifier.rsplit('@', 1)[-1]
        return any(i.startswith('email:') and i.rsplit('@', 1)[-1] not in self.keys.freemail | {domain}
                   for i in self.union.members[self.union.find(chat)])

    def _rivals(self, chat, identifier, made):
        """Whether anyone else in touch with the owner in those days could be who booked: the same first name, no other
        surname, and not known at another company's address."""
        mine = {self.union.find(chat), self.union.find(identifier)}
        domain, names = identifier.rsplit('@', 1)[-1], self.names.get(identifier) or self.chat_words[chat][:1]
        for _, at, _, m, found in self.per_event.values():
            if not dt.timedelta(0) <= made - at <= SURE:
                continue
            for i, _, _, role in found:
                if role == 'seen' or self.union.find(i) in mine:
                    continue
                words = self.chat_words.get(i) or self.names.get(i) or local_words(i[6:])[:1] if i.startswith('email:') else self.chat_words.get(i)
                if words and words[0] == names[0] and name_match(words, names) and not any(
                        x.startswith('email:') and x.rsplit('@', 1)[-1] not in self.keys.freemail | {domain}
                        for x in self.union.members[self.union.find(i)]):
                    return True
        return False


def _names(text, names):
    """Whether a text names one of these companies: a domain's own letters, as one to three words ("Blue Harbor" at
    blueharbor.example) or as its address."""
    words = re.findall(r'[a-z0-9]+', folded_words(text))
    return any(''.join(words[i:i + n]) in names for i in range(len(words)) for n in (1, 2, 3))
