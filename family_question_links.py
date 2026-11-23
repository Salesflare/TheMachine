"""Which of the owner's messages may be on the same matter as the ones an answer to a family member comes from
(family_questions.py), and which mail can be believed at all: by threads, order numbers, senders and addresses, in code."""
from __future__ import annotations

import datetime as dt
import json
import re

import family_question_sources as fqs
import shared_graph_private
import verified_sender
from machine import kinds
from machine.text import QUOTED_MARK

MAIL = tuple(k for k, row in kinds.KINDS.items() if row['service'] in ('gmail', 'outlook') and row['family'] == kinds.MAIL)
SCAN = 3000           # mails of the last fqs.DAYS days it looks through
WORDS = (r'order|bestelling|bestelnummer|commande|bestellung|bestellnummer|pedido|ordine|encomenda|booking|reservation|reservering|boeking|'
         r'réservation|buchung|reserva|prenotazione|tracking|track|trace|shipment|parcel|zending|pakket|barcode|colis|suivi|sendung|paket|'
         r'sendungsnummer|envío|seguimiento|spedizione|rastreio')
NUMBER = re.compile(rf'(?i)(?:\b(?:{WORDS})(?:\s*(?:number|nummer|nr|no|id|code|num[ée]ro|n°|#))?[.:\s#-]*|#\s?)([A-Z0-9][A-Z0-9-]{{2,}})')
CODE = re.compile(r'(?<![\w-])[A-Z]{2,4}-\d{2,}(?![\w-])')
TITLE_NUMBER = re.compile(r'(?i)(?<![\w-])(?:[A-Z]{1,5}-?)?\d{4,}(?![\w-])')
QUOTE = re.compile(r'(?im)^\s*>|^\s*(?:on|op|le|am|el|il|em)\b.{4,120}\b(?:wrote|schreef|écrit|schrieb|escribió|scritto|escreveu)\s*:|^\s*-{3,}\s*(?:original|forwarded|'
                   r'oorspronkelijk|doorgestuurd)|^\s*(?:from|van|de|von|da)\s*:\s')
STOP = frozenset('''about after again also back been before being both come coming could does doing done down each ever every from gone good have
having hear heard here into just know known last later like look made make many mine more most much need never news next once only open order
other ours over please really right said same seen send sent shall shipped should soon still such sure take tell than thank thanks that their them
then there these they thing things this those through time today tomorrow told took under until update upon very want was week well were what when
where which while will with without would year yesterday your yours monday tuesday wednesday thursday friday saturday sunday month delivery
delivered deliver arrive arrives arrived arriving package parcel already anything something someone expected booked booking bought ordered
weet weten nieuws wanneer waar welke hoeveel komt komen kwam gekomen heeft hebben hebt jouw onze deze voor naar over alles iets nog altijd vandaag
morgen gisteren bestelling besteld levering geleverd pakje pakket zijn worden wordt werd kunnen moet moeten gaat goed
quand nouvelles commande livraison livré colis avec pour dans notre votre cette être avoir fait sera demain
wann neuigkeiten bestellung lieferung geliefert paket haben unser unsere kommt heute'''.split())


def tokens(text):
    return {w for w in re.findall(r'[^\W\d_]{4,}', str(text or '').casefold()) if w not in STOP}


def numbers(row):
    """A mail's order, booking and tracking numbers."""
    text = f"{row['title']}\n{row['body']}"
    found = NUMBER.findall(text) + CODE.findall(text) + TITLE_NUMBER.findall(str(row['title'] or ''))
    return {m.strip('-').upper() for m in found if sum(c.isdigit() for c in m) >= 2 and not re.fullmatch(r'(?:19|20)\d\d(?:-?\d{2}){0,2}', m.strip('-'))}


def addresses(value):
    out = []
    for part in value if isinstance(value, list) else [value]:
        out += [a.lower() for a in shared_graph_private.ADDRESS.findall(str(part or ''))]
    return out


def given(meta):
    """Who a mail was sent to."""
    return set(addresses(meta.get('to')) + addresses(meta.get('cc')))


def own_words(body):
    """What someone wrote themselves in a message: nothing quoted or forwarded under it."""
    text = str(body or '')
    for cut in (QUOTED_MARK, QUOTE):
        found = cut.search(text)
        text = text[:found.start()] if found else text
    return text


def automated(meta):
    return shared_graph_private.automated_message(meta)


def sent(meta, mine):
    """Whether the owner wrote a mail themselves: from one of their addresses, and in their sent mail."""
    sender = addresses(meta.get('from'))
    return 'SENT' in (meta.get('labels') or ()) and bool(sender) and sender[0] in mine


def poses(row, name, emails):
    """Whether a mail bears the asker's name and not their address."""
    sender = str(fqs._meta(row).get('from') or '')
    return row['kind'] in MAIL and bool(name & set(re.findall(r'[^\W\d_]+', sender.partition('<')[0].casefold()))) and not set(addresses(sender)[:1]) & set(emails)


def alike(one, other):
    """Whether one domain could pass for another: r0yer.example or royer-service.example for royer.example."""
    a, b = (d.rpartition('.')[0] for d in (one, other))
    if a == b or min(len(a), len(b)) < 6:
        return False
    if set(a.split('-')) > set(b.split('-')):  # the other's name with a word more; not a part of it, like mail.royer.example
        return True
    a, b = (d.replace('-', '').replace('rn', 'm').replace('vv', 'w').translate(str.maketrans('01i', 'oll')) for d in (a, b))
    at = next((n for n, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
    return a[at + 1:] in (b[at + 1:], b[at:]) or a[at:] == b[at + 1:]  # one letter other, more or less


def believed(row, every, mine, asker):
    """Whether an answer may come from this mail: the owner wrote it, its sender's address is verified, or the owner wrote
    in its thread. Never the asker's own words, nor an address that could pass for another one in the owner's mail."""
    meta = fqs._meta(row)
    thread = meta.get('thread_id')
    domain = ''.join(addresses(meta.get('from'))[:1]).rpartition('@')[2]
    if re.search(r'[a-z][01](?=[a-z.])', domain.rpartition('.')[0] + '.') or any(alike(domain, other) for other in {''.join(addresses(fqs._meta(r).get('from'))[:1]).rpartition('@')[2] for r in every}):
        return False
    return not set(addresses(meta.get('from'))[:1]) & set(asker['emails']) and (
        meta.get(verified_sender.KEY) is True or sent(meta, mine) or bool(thread) and any(
            (m := fqs._meta(r)).get('thread_id') == thread and r['account_id'] == row['account_id'] and sent(m, mine) for r in every))


def mailed(db, store, accounts, clock):
    """The owner's personal mail of the last fqs.DAYS days, newest first."""
    found = [r[0] for r in db.execute(
        'SELECT id FROM events WHERE deleted=0 AND occurred_at>=? AND account_id IN (SELECT value FROM json_each(?)) AND kind IN (SELECT value FROM json_each(?)) '
        'ORDER BY occurred_at DESC LIMIT ?', ((clock - dt.timedelta(days=fqs.DAYS)).isoformat(), json.dumps(accounts), json.dumps(MAIL), SCAN))]
    return list(store.events(accounts, kinds=list(MAIL), event_ids=found)) if found else []


def sender_named(row, text):
    """Whether a text names who sent a mail: by its domain, or by the name the sender gives itself."""
    meta = fqs._meta(row)
    found = addresses(meta.get('from'))
    labels = found[0].rpartition('@')[2].split('.')[:-1] if found else []
    squeezed = re.sub(r'[\W_]', '', text.casefold())
    name = tokens(re.sub(r'<[^>]*>\s*$', '', str(meta.get('from') or '')))
    return any(len(w) >= 6 and w.replace('-', '') in squeezed for w in labels) or any(len(w) >= 5 for w in name) and name <= tokens(text)


def named_elsewhere(place, row, every):
    """Whether mail of somebody else than this one's sender names the same address or vehicle: the household's own does."""
    squeeze = lambda text: re.sub(r'\W', '', text.casefold())
    domain = lambda r: ''.join(addresses(fqs._meta(r).get('from'))[:1]).rpartition('@')[2]
    return any(squeeze(place) in squeeze(f"{r['title']} {r['body']}") for r in every if domain(r) != domain(row))


def linked(db, rows, every, text=''):
    """{event id: thread | order | sender} of what may be on the same matter as these rows: their threads, the mails with
    one of their order numbers, and those of a company that they, or text, name. every: mailed's, newest first."""
    out = {}
    for e in set().union(*fqs._threads(db, rows).values()) if rows else ():
        out.setdefault(e, 'thread')
    known = {r['id']: numbers(r) for r in [*rows, *every]}
    shared = set().union(*(known[r['id']] for r in rows)) if rows else set()
    for r in every:
        if known[r['id']] & shared:
            out.setdefault(r['id'], 'order')
    senders = {a[0].rpartition('@')[2] for r in rows if automated(fqs._meta(r)) and (a := addresses(fqs._meta(r).get('from')))}
    said = ' '.join([text, *(f"{r['title']} {own_words(r['body'])}" for r in rows)])
    for r in every:
        meta, theirs = fqs._meta(r), f"{r['title']} {own_words(r['body'])}"
        company = 'SENT' not in (meta.get('labels') or ()) and ((addresses(meta.get('from')) or [''])[0].rpartition('@')[2] in senders or sender_named(r, said))
        if company or any(automated(fqs._meta(c)) and sender_named(c, theirs) for c in rows):
            out.setdefault(r['id'], 'sender')
    return out


def moment(at):
    found = dt.datetime.fromisoformat(str(at))
    return found if found.tzinfo else found.replace(tzinfo=dt.timezone.utc)
