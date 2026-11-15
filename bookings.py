"""Bookings in mail: the travel and ticket reservations a confirmation mail carries as structured data, read with plain code.

Airlines, hotels, rail, bus and car rental companies, ticket sellers and booking sites put a schema.org reservation in
their mail so mail apps can show it, as JSON-LD (a <script type="application/ld+json"> block) or as microdata
(itemscope, itemtype and itemprop attributes on the mail's own HTML; many airlines and hotels use this): FlightReservation,
LodgingReservation, TrainReservation, BusReservation, BoatReservation, RentalCarReservation and EventReservation. read()
turns those into short, flat rows that the mail source keeps in the message's metadata (sealed at rest with the rest of
it, message_seal.py). A trip note (trip_notes.py) is built from the travel rows, an event note (event_notes.py) from
the event rows (name: the event; where: its venue and town; guests: how many seats). Nothing is guessed: a mail without the structured data gives nothing,
and a reservation without a start time is left out.

A row: {type, code, status, start, end, from, to, name, number, by, seat, ticket, guests, where}. start and end are
local wall-clock times as the booking states them ('2026-12-02T07:10', or a day), so a flight shows the time on the
ticket wherever the owner reads it. No link is kept (a manage-booking link can sign someone in)."""
import html
import html.parser
import json
import re

TYPES = {'FlightReservation': 'flight', 'LodgingReservation': 'hotel', 'TrainReservation': 'train',
         'BusReservation': 'bus', 'BoatReservation': 'boat', 'RentalCarReservation': 'car', 'EventReservation': 'event'}
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
                   name=_text(what.get('name')), where=_text(address.get('addressLocality')), guests=_text(thing.get('numGuests')))
    elif kind == 'car':
        company = what.get('rentalCompany') or what.get('brand') or thing.get('provider')
        row.update(start=_when(thing.get('pickupTime')), end=_when(thing.get('dropoffTime')),
                   **{'from': _place(thing.get('pickupLocation')), 'to': _place(thing.get('dropoffLocation'))},
                   by=_text(company), name=_text(what.get('name')))
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
    if kind not in ('hotel', 'event') and not (row.get('from') or row.get('to')):
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
