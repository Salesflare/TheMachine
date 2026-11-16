"""Bookings in mail: the travel and ticket reservations a confirmation mail carries, as short flat rows.

Two ways in:
- Structured data, read with plain code (read): airlines, hotels, rail, bus and car rental companies, ticket sellers and
  booking sites put a schema.org reservation in their mail so mail apps can show it, as JSON-LD (a <script
  type="application/ld+json"> block) or as microdata (itemscope, itemtype and itemprop attributes on the mail's own
  HTML): FlightReservation, LodgingReservation, TrainReservation, BusReservation, BoatReservation, RentalCarReservation,
  TaxiReservation and EventReservation. The mail source keeps the rows in the message's metadata (sealed at rest with
  the rest of it, message_seal.py).
- Many confirmations carry none (a holiday home, a parking, a rail ticket, a forward, a smaller hotel or airline). A
  mail without it that looks like a booking (looks_booked: a confirmation word, something to travel to or attend, a
  date and a code, plain code) is read by a small model call instead (extract_prompt, TripsApp.trip_extract_step), a
  few mails per call, its answer checked field by field (parse, checked) into the same rows.

A trip (trip_notes.py) is built from the travel rows, an event (event_notes.py) from the event rows (name: the event;
where: its venue and town; guests: how many seats). A reservation without a start time is left out.

A row: {type, code, status, start, end, from, to, name, number, by, seat, ticket, guests, where, address}; type is one
of KINDS. start and end are local wall-clock times as the booking states them ('2026-12-02T07:10', or a day), so a
flight shows the time on the ticket wherever the owner reads it. A row from the model has read: 'text', and others: 1
when it names other people and not the owner (a colleague's booking forwarded). No link is kept (a manage-booking link
can sign someone in)."""
import html
import html.parser
import json
import re

TYPES = {'FlightReservation': 'flight', 'LodgingReservation': 'hotel', 'TrainReservation': 'train', 'BusReservation': 'bus',
         'BoatReservation': 'boat', 'RentalCarReservation': 'car', 'TaxiReservation': 'taxi', 'EventReservation': 'event'}
ROWS_MAX = 12  # per message
TEXT_MAX = 120
SCRIPT = re.compile(r'<script\b[^>]*type\s*=\s*["\']?application/ld\+json["\']?[^>]*>(.*?)</script\s*>', re.I | re.S)
WHEN = re.compile(r'(\d{4}-\d{2}-\d{2})(?:[T ](\d{2}:\d{2}))?')
BLOCK_MAX = 200_000


def _text(value):
    """A name or a code: plain words, short; a thing ({name}) gives its name."""
    if isinstance(value, dict):
        value = value.get('name') or value.get('iataCode') or ''
    if isinstance(value, list):
        value = value[0] if value else ''
    if not isinstance(value, (str, int, float)) or isinstance(value, bool):
        return ''
    return ' '.join(html.unescape(str(value)).split())[:TEXT_MAX]


def _when(value):
    """The booking's own wall-clock time ('2026-12-02T07:10') or day, without its offset; '' when there is none."""
    m = WHEN.match(str(value or '').strip())
    if not m:
        return ''
    return m[1] + ('T' + m[2] if m[2] else '')


def _place(value):
    """Where: a city when the booking names one, else the airport, station or place's own name."""
    if not isinstance(value, dict):
        return _text(value)
    address = value.get('address')
    city = _text(address.get('addressLocality')) if isinstance(address, dict) else ''
    return city or _text(value.get('name')) or _text(value.get('iataCode'))


def _street(address):
    """A postal address as one line: street, then town."""
    if not isinstance(address, dict):
        return _text(address)
    parts = [_text(address.get(k)) for k in ('streetAddress', 'postalCode', 'addressLocality')]
    return ', '.join(x for x in (parts[0], ' '.join(x for x in parts[1:] if x)) if x)[:TEXT_MAX] if parts[0] else ''


def _things(found):
    """Every dict in a JSON-LD block: a list, an @graph, or one thing."""
    if isinstance(found, list):
        for x in found:
            yield from _things(x)
    elif isinstance(found, dict):
        if isinstance(found.get('@graph'), list):
            yield from _things(found['@graph'])
        else:
            yield found


def _kind(thing):
    kind = thing.get('@type')
    if isinstance(kind, list):
        kind = next((k for k in kind if k in TYPES), None)
    return TYPES.get(str(kind or '').rsplit('/', 1)[-1])


def _status(thing):
    status = str(thing.get('reservationStatus') or '').rsplit('/', 1)[-1].lower()
    return 'canceled' if 'cancel' in status else 'confirmed'


def _row(thing):
    kind = _kind(thing)
    if not kind:
        return None
    what = thing.get('reservationFor') if isinstance(thing.get('reservationFor'), dict) else {}
    row = {'type': kind, 'code': _text(thing.get('reservationNumber')), 'status': _status(thing)}
    ticket = thing.get('reservedTicket')
    ticket = ticket[0] if isinstance(ticket, list) and ticket else ticket  # an event's tickets: the first one's number and seat
    ticket = ticket if isinstance(ticket, dict) else {}
    seat = ticket.get('ticketedSeat') if isinstance(ticket.get('ticketedSeat'), dict) else {}
    if kind == 'flight':
        airline = what.get('airline') if isinstance(what.get('airline'), dict) else {}
        number = _text(what.get('flightNumber'))
        code = _text(airline.get('iataCode'))
        row.update(start=_when(what.get('departureTime')), end=_when(what.get('arrivalTime')),
                   **{'from': _place(what.get('departureAirport')), 'to': _place(what.get('arrivalAirport'))},
                   number=(code + ' ' + number if code and not number.upper().startswith(code.upper()) else number).strip(),
                   by=_text(airline.get('name')), seat=_text(thing.get('airplaneSeat')) or _text(seat.get('seatNumber')))
    elif kind == 'hotel':
        address = what.get('address') if isinstance(what.get('address'), dict) else {}
        row.update(start=_when(thing.get('checkinTime') or thing.get('checkinDate')), end=_when(thing.get('checkoutTime') or thing.get('checkoutDate')),
                   name=_text(what.get('name')), where=_text(address.get('addressLocality')), guests=_text(thing.get('numGuests')),
                   address=_street(address))
    elif kind == 'car':
        company = what.get('rentalCompany') or what.get('brand') or thing.get('provider')
        pickup = thing.get('pickupLocation') if isinstance(thing.get('pickupLocation'), dict) else {}
        row.update(start=_when(thing.get('pickupTime')), end=_when(thing.get('dropoffTime')),
                   **{'from': _place(thing.get('pickupLocation')), 'to': _place(thing.get('dropoffLocation'))},
                   by=_text(company), name=_text(what.get('name')), address=_street(pickup.get('address')))
    elif kind == 'taxi':  # a taxi or an airport transfer: where it picks up, at what time
        row.update(start=_when(thing.get('pickupTime')), **{'from': _place(thing.get('pickupLocation')), 'to': _place(thing.get('dropoffLocation'))},
                   by=_text(thing.get('provider') or what.get('provider')), guests=_text(thing.get('partySize')))
    elif kind == 'event':  # a concert, a match, a festival, a conference: where it is, the venue and its town
        place = what.get('location')
        place = place[0] if isinstance(place, list) and place else place
        place = place if isinstance(place, dict) else {}
        address = place.get('address') if isinstance(place.get('address'), dict) else {}
        where = [x for x in (_text(place.get('name')), _text(address.get('addressLocality'))) if x]
        row.update(start=_when(what.get('startDate')), end=_when(what.get('endDate')), name=_text(what.get('name')),
                   where=', '.join(dict.fromkeys(where)), by=_text(thing.get('provider')), guests=_text(thing.get('numSeats')),
                   seat=' '.join(x for x in (_text(seat.get('seatSection')), _text(seat.get('seatRow')), _text(seat.get('seatNumber'))) if x))
    else:  # train, bus, boat
        place = {'train': ('departureStation', 'arrivalStation'), 'bus': ('departureBusStop', 'arrivalBusStop'),
                 'boat': ('departureBoatTerminal', 'arrivalBoatTerminal')}[kind]
        number = _text(what.get({'train': 'trainNumber', 'bus': 'busNumber', 'boat': 'name'}[kind]))
        row.update(start=_when(what.get('departureTime')), end=_when(what.get('arrivalTime')),
                   **{'from': _place(what.get(place[0])), 'to': _place(what.get(place[1]))},
                   number=number, by=_text(what.get('provider') or thing.get('provider') or what.get('busCompany')),
                   seat=' '.join(x for x in (_text(seat.get('seatSection')), _text(seat.get('seatNumber'))) if x))
    row['ticket'] = _text(ticket.get('ticketNumber'))
    if not row.get('start'):
        return None
    if kind in ('hotel', 'event') and not row.get('name'):
        return None
    if kind not in ('hotel', 'event') and not (row.get('from') or row.get('to')):  # a ride, a rental car, a taxi
        return None
    return {k: v for k, v in row.items() if v}


def _json(block):
    """The block as JSON; a mail that escaped it as HTML (&quot;) is read unescaped."""
    for text in (block, html.unescape(block)):
        try:
            return json.loads(text)
        except ValueError:
            continue
    return None


VOID = frozenset('area base br col embed hr img input link meta param source track wbr'.split())
MICRODATA = re.compile(r'itemtype\s*=\s*["\']?https?://schema\.org/[A-Za-z]*Reservation', re.I)
PART_MAX = 2_000_000  # characters of one HTML part read for microdata


class _Microdata(html.parser.HTMLParser):
    """schema.org microdata (itemscope, itemtype, itemprop) as the same things JSON-LD gives: {'@type', prop: value},
    a nested item as a dict, the first value of a property kept. A value is the element's content, datetime, href or
    src attribute, else its text."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items, self.stack = [], []  # stack: [tag, item it opens or None, (owner, props) collecting text or None, text]

    def _owner(self):
        return next((e[1] for e in reversed(self.stack) if e[1] is not None), None)

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or '') for k, v in attrs}
        props, owner = a.get('itemprop', '').split(), self._owner()
        if 'itemscope' in a:
            item = {'@type': a.get('itemtype', '').split()[0].rsplit('/', 1)[-1] if a.get('itemtype', '').split() else ''}
            if props and owner is not None:
                for p in props:
                    owner.setdefault(p, item)
            else:
                self.items.append(item)
            if tag not in VOID:
                self.stack.append([tag, item, None, []])
            return
        if not props or owner is None:
            if tag not in VOID:
                self.stack.append([tag, None, None, []])
            return
        value = next((a[k] for k in ('content', 'datetime', 'href', 'src') if k in a), None)
        if value is not None or tag in VOID:
            for p in props:
                owner.setdefault(p, ' '.join(str(value or '').split()))
            if tag not in VOID:
                self.stack.append([tag, None, None, []])
            return
        self.stack.append([tag, None, (owner, props), []])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self._pop()

    def handle_endtag(self, tag):
        if tag in VOID or not any(e[0] == tag for e in self.stack):
            return  # a stray end tag: mail HTML is often loose
        while self.stack and self._pop() != tag:
            pass

    def _pop(self):
        tag, _, collecting, text = self.stack.pop()
        if collecting:
            owner, props = collecting
            for p in props:
                owner.setdefault(p, ' '.join(''.join(text).split()))
        return tag

    def handle_data(self, data):
        for e in self.stack:
            if e[2]:
                e[3].append(data)

    def close(self):
        super().close()
        while self.stack:
            self._pop()


def _microdata(part):
    """The top-level microdata items of one HTML part; none when it names no schema.org reservation."""
    if not MICRODATA.search(part):
        return []
    reader = _Microdata()
    try:
        reader.feed(part[:PART_MAX])
        reader.close()
    except Exception:  # noqa: BLE001 - a part the parser can't read gives nothing; nothing is guessed
        return []
    return reader.items


_M = (r'jan|feb|m[aä]r|apr|ma[iy]|mei|jun|jul|aug|sep|o[ck]t|nov|de[cz]|janv|f[eé]v|avr|mai|juin|juil|ao[uû]t|d[eé]c|ene|abr|ago|dic|'
      r'gen|giu|lug|set|ott|maart|juni|juli|januari|februari|augustus|september|oktober|november|december')
BOOKED = re.compile(r'confirm|bevestig|best[aä]tig|\breserv(ation|ering|ierung|a)\b|r[eé]servation|boeking|booking|buchung|'
                    r'prenotazion|itinerar|reisoverzicht|e-?ticket|\btickets?\b|boarding ?pass|instapkaart|bordkarte|'
                    r'embarque|your (trip|stay|ride|rental|car)\b|je (reis|verblijf)\b|online aankoop', re.I)
TRAVEL = re.compile(r'flight|vlucht|vuelo|\bvolo\b|\bflug|boarding|instapkaart|hotel|airbnb|check-?in|incheck|accommodat|'
                    r'verblijf|resort|vakantiepark|camping|\btrain\b|trein|\bzug\b|\btren\b|treno|bus ?ticket|busreis|ferry|'
                    r'veerboot|car rental|rental car|rent a car|huurauto|mietwagen|pick-?up location|parking|parkeren|'
                    r'airport transfer|taxi|airport|luchthaven|flughafen|a[eé]roport|aeropuerto|concert|festival|museum|'
                    r'excursi|attractie|attraction|pretpark|theme park|dierentuin|\bzoo\b|cinema|bioscoop|theater|theatre', re.I)
DATED = re.compile(r'\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b|\b\d{4}-\d{2}-\d{2}\b|'
                   rf'\b\d{{1,2}}\.? ?(?:{_M})[a-zé]*\.?,? ?(?:\d{{4}})?\b|\b(?:{_M})[a-zé]*\.? \d{{1,2}}\b', re.I)
_CODE = r'(?=[A-Z0-9-]*\d)(?=[A-Z0-9-]*[A-Z])[A-Z0-9][A-Z0-9-]{4,13}\b|\d{6,14}\b|[A-Z]{6}\b'
CODED = re.compile(rf'(?:booking|reserv\w*|r[eé]servation|confirmation|bevestigings?|boekings?|buchungs?|order|bestel|ticket|'
                   rf'pnr|dossier|referen\w*|prenotazione|localizador|code|nummer|number|nr)\W{{0,3}}(?:\w+\W{{1,3}}){{0,2}}(?:{_CODE})', re.I)
CODED_TITLE = re.compile(rf'\b(?:{_CODE})')
NOT_BOOKED = re.compile(r'verification code|verificatiecode|one-time password|\bOTP\b|code de v[eé]rification|'
                        r'how was your|review|survey|beoordeel|rate your|newsletter|nieuwsbrief|webinar|% ?(off|korting)|'
                        r'\bdeals?\b|aanbieding|last minute|price alert|tracked flight|is now €|receipt|payment|invoice|'
                        r'factuur|betaling|subscription|abonnement|save \d|order receipt', re.I)
FORWARD = re.compile(r'^\s*(fwd?|fw|tr|wg|rv|i)\s*:', re.I)


def looks_booked(title, sender, text, own=()):
    """Whether a mail without structured data looks like a booking a model may read (extract): a confirmation word,
    something to travel to or attend, a date and a code. Plain code, to keep the model's reading to the few mails that
    can hold one. own: the owner's addresses; their own mail counts only when it forwards one."""
    title, text = str(title or ''), str(text or '')
    if NOT_BOOKED.search(title):
        return False
    if any(a and a.casefold() in str(sender or '').casefold() for a in own) and not FORWARD.match(title):
        return False
    head, body = title + '\n' + text[:2000], text[:6000]
    return bool(BOOKED.search(head) and TRAVEL.search(title + '\n' + body) and DATED.search(title + '\n' + body)
                and (CODED_TITLE.search(title) or CODED.search(body)))


KINDS = ('flight', 'train', 'bus', 'boat', 'hotel', 'car', 'taxi', 'parking', 'event')
FIELDS = ('code', 'start', 'end', 'from', 'to', 'name', 'where', 'address', 'number', 'by', 'seat', 'ticket', 'guests')
MAIL_CHARS = 3500  # of one mail's text in a prompt: a confirmation's details come first, its small print after
LINK = re.compile(r'https?://\S+|<https?://[^>]*>|\[https?://[^\]]*\]')


def clean(text):
    """A mail's text for the prompt: no links (a manage-booking link can sign someone in), no empty lines, short."""
    text = LINK.sub('', html.unescape(str(text or '')))
    lines = [' '.join(x.split()) for x in text.splitlines()]
    return '\n'.join(x for x in lines if x and not set(x) <= set('-=_*|>'))[:MAIL_CHARS]


def extract_prompt(mails, owner=''):
    """The prompt that reads bookings from mail without structured data: mails [{id, title, sender, text}]. The
    answer is JSON only, checked by parse()."""
    shown = '\n\n'.join(f'<<<MAIL {m["id"]}\nSubject: {m["title"]}\nFrom: {m["sender"]}\nSent: {str(m.get("occurred_at") or "")[:10]}\n\n'
                        f'{clean(m["text"])}\n>>>' for m in mails)
    who = f'The owner is {owner}. ' if owner else ''
    return f'''Read travel bookings and tickets from these emails. This is a background task of the personal-assistant service; answer with JSON only.

{who}For each email, list what it books for the owner: a flight, train, bus or ferry ride (one per leg), a hotel, holiday home or other stay, a rental car, a taxi or airport transfer, airport or station parking, or a ticket for an event or activity (a tour, a museum, a show, a match). Only what is booked: a confirmation, a ticket, an itinerary, a change or a cancellation. Nothing from ads, offers, newsletters, price alerts, searches, surveys, receipts for other things, or verification codes; an email with none gives [].

Copy values as the email writes them; never guess. Leave a value out when the email doesn't give it.
- type: flight, train, bus, boat, hotel, car, taxi, parking or event.
- status: "canceled" when the email cancels it, else "confirmed".
- code: the booking code or reservation number.
- start, end: local times as on the booking, "YYYY-MM-DDTHH:MM", or "YYYY-MM-DD" when there is no time (never 00:00 for a time it doesn't give). A day without a year is the first such day after the email was sent. A connecting leg without its own day or time has the day of the leg before it. A ride: departure and arrival. A stay: check-in and check-out. A rental car or parking: pick-up and return. An event: its start and end.
- from, to: a ride's or taxi's departure and arrival city, airport or station, as named; a rental car's pick-up and return place.
- name: the hotel's or stay's name, the event's name, the parking's name.
- where: the town of a stay, an event or a parking.
- address: the street address of a stay, an event, a parking, or a rental car's pick-up desk.
- number: a flight or train number (like "EX 3410").
- by: the airline, rail or bus company, rental company or ticket seller.
- seat, ticket, guests: the owner's seat, ticket number, and how many guests or tickets.
- owner_on_it: "yes" when the owner is named as a passenger, guest or driver, "no" when others are named and the owner is not, else "unknown".

Answer: {{"<id after MAIL>": [{{"type": "...", ...}}], ...}} with every email's id, like {{"{mails[0]["id"] if mails else 1}": []}}.

{shown}'''


def _parse_json(reply):
    text = str(reply or '').strip()
    if text.startswith('```'):
        text = text.strip('`').split('\n', 1)[-1].rsplit('```', 1)[0]
    start = text.find('{')
    try:
        found = json.loads(text[start:text.rfind('}') + 1]) if start >= 0 else None
    except ValueError:
        return None
    return found if isinstance(found, dict) else None


def checked(item):
    """One booking from the model as the same flat row read() gives, or None when it isn't one: a known type, a start
    in the booking's own time, and what that type needs (a name for a stay or an event, a place for the rest)."""
    if not isinstance(item, dict) or item.get('type') not in KINDS:
        return None
    row = {'type': item['type'], 'status': 'canceled' if str(item.get('status') or '').lower().startswith('cancel') else 'confirmed'}
    for key in FIELDS:
        value = _when(item.get(key)) if key in ('start', 'end') else _text(item.get(key))
        if key in ('start', 'end') and value and value.endswith('T00:00'):
            value = value[:10]  # a time the mail didn't give, read as midnight: the day alone
        elif value and key not in ('start', 'end'):
            value = re.sub(r'\s*,(?:\s*,)+', ',', value).strip(' ,')  # "Avenue 10,, 6220": one comma
        if value:
            row[key] = value
    if str(item.get('owner_on_it') or '').lower() == 'no':
        row['others'] = 1  # someone else's booking: it can join the owner's trip, never make one (trip_notes.journeys)
    if row['status'] == 'canceled' and row.get('code'):
        return row  # a cancellation names its code; the rest may be gone
    if not row.get('start') or (row['type'] in ('hotel', 'event') and not row.get('name')):
        return None
    if row['type'] not in ('hotel', 'event', 'parking') and not (row.get('from') or row.get('to')):
        return None
    if row['type'] == 'parking' and not (row.get('name') or row.get('where') or row.get('address')):
        return None
    return row


def parse(reply, ids):
    """The model's answer as {mail id: [rows]} for the mails asked about; None when the answer isn't one (asked again
    later). A mail it left out has no bookings."""
    found = _parse_json(reply)
    if found is None:
        return None
    found = {re.sub(r'(?i)^\W*mail\W*', '', str(k)).strip(): v for k, v in found.items()}  # "MAIL 12" is mail 12
    out = {}
    for i in ids:
        items = found.get(i) if isinstance(found.get(i), list) else []
        rows, seen = [], set()
        for item in items:
            row = checked(item)
            same = json.dumps(row, sort_keys=True)
            if row and same not in seen and len(rows) < ROWS_MAX:
                seen.add(same)
                rows.append({**row, 'read': 'text'})
        out[i] = rows
    return out


def read(html_parts):
    """The reservations in a mail's HTML parts, each once, in the order the mail lists them: JSON-LD blocks first, then
    microdata (many airlines and hotels mark up their confirmations that way)."""
    rows, seen = [], set()
    for part in html_parts or ():
        part = str(part or '')
        found_all = []
        for block in SCRIPT.findall(part):
            if len(block) > BLOCK_MAX:
                continue
            found = _json(block.strip())
            if found is not None:
                found_all.append(found)
        found_all.append(_microdata(part))
        for found in found_all:
            for thing in _things(found):
                row = _row(thing)
                if not row:
                    continue
                same = json.dumps(row, sort_keys=True)
                if same not in seen and len(rows) < ROWS_MAX:
                    seen.add(same)
                    rows.append(row)
    return rows
