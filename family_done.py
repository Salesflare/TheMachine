"""Already did this, in a Family Fleet (docs/family.md): which to-dos of two members are the same one, and the quiet
line an open one gets when another member closed theirs as done. Plain code over the owner's own rows; fleet.py's
handled_round sends and looks up the keyed hashes (family.DONE is the rule) and writes the line.

Same to-do: the same email (its Message-ID, whoever it went to: a Machine without that email can't match its hash), the
same bill (bill_of: an IBAN and a payment reference, both checked) or the same form (forms_of: one online form's link,
so a reminder that came as a new email still matches the to-do done from the first one). The line says who and when,
never more, and nothing closes by itself: the owner taps Done or Still needed."""
from __future__ import annotations

import json
import re

import message_seal

SAME = object()  # line(): leave done_elsewhere as it is

IBAN = re.compile(r'\b([A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){2,7}(?: ?[A-Z0-9]{1,3})?)\b')
OGM = re.compile(r'(?:\+{3}|\*{3})\s*(\d{3})\s*/\s*(\d{4})\s*/\s*(\d{5})\s*(?:\+{3}|\*{3})')  # a Belgian structured reference
RF = re.compile(r'\bRF\s?(\d{2})((?: ?[A-Z0-9]){1,21})\b')  # an ISO 11649 creditor reference
FORM = re.compile(r'https?://((?:forms\.gle/|docs\.google\.com/forms/(?:u/\d+/)?d/(?:e/)?)[A-Za-z0-9_-]{8,}'
                  r'|forms\.(?:office|microsoft)\.com/(?:r/[A-Za-z0-9]{6,}|Pages/ResponsePage\.aspx\?id=[A-Za-z0-9_-]{8,})'
                  r'|[a-z0-9-]+\.typeform\.com/to/[A-Za-z0-9]{4,}|tally\.so/r/[A-Za-z0-9]{4,}|form\.jotform\.com/\d{6,})', re.I)
FORM_SPREAD = 5  # a form link in more of the owner's emails than this is a standing one (a newsletter footer): never a match


def _mod97(text):
    """ISO 7064 mod 97 of letters (A=10 ... Z=35) and digits."""
    return int(''.join(str(int(c, 36)) for c in text)) % 97


def _iban(raw):
    """The IBAN at the start of raw, if one checks out: the pattern may run on into a next word ("... 6909 PAYEE")."""
    value = raw.replace(' ', '')
    return next((value[:n] for n in range(min(len(value), 34), 14, -1) if _mod97(value[4:n] + value[:4]) == 1), None)


def bill_of(text):
    """The bill a text is about, as 'IBAN|reference', when it gives both and both check out: an IBAN (mod 97) and a
    payment reference (a Belgian +++123/4567/89012+++ or an RF creditor reference). Two members' to-dos for the same
    bill match on it, whatever email each came from. None without both: an IBAN alone (a supplier's every invoice)
    says too little."""
    text = str(text or '').upper()
    iban = next((found for found in (_iban(m.group(1)) for m in IBAN.finditer(text)) if found), None)
    if not iban:
        return None
    reference = None
    for m in OGM.finditer(text):
        digits = ''.join(m.groups())
        if (int(digits[:10]) % 97 or 97) == int(digits[10:]):
            reference = digits
            break
    if not reference:
        for m in RF.finditer(text):
            body = m.group(2).replace(' ', '')
            if _mod97(body + 'RF' + m.group(1)) == 1:
                reference = 'RF' + m.group(1) + body
                break
    return f'{iban}|{reference}' if reference else None


def forms_of(text):
    """The online forms a text links to (Google, Microsoft, Typeform, Tally, Jotform), as host/path without the scheme:
    the host in lower case, the form's id as written (ids are case-sensitive)."""
    found = []
    for m in FORM.finditer(str(text or '')):
        host, _, path = m.group(1).partition('/')
        found.append(host.lower() + '/' + path)
    return list(dict.fromkeys(found))


def _spread(db, form):
    """How many of the owner's signals carry this form's id (full-text search), capped just past FORM_SPREAD."""
    words = re.findall(r'[A-Za-z0-9]+', form.rsplit('/', 1)[-1].rsplit('=', 1)[-1])
    if not words:
        return FORM_SPREAD + 1
    try:
        return db.execute('SELECT count(*) FROM (SELECT rowid FROM event_search WHERE event_search MATCH ? LIMIT ?)',
                          (message_seal.match(db, words, ' AND '), FORM_SPREAD + 1)).fetchone()[0]
    except Exception:  # no search index (an old store): the form alone can't say it's one matter
        return FORM_SPREAD + 1


def sources(db, card):
    """What makes two members' to-dos the same one: the Message-IDs of its emails (up to 5), its bill as
    'bill:IBAN|reference' and its forms as 'form:host/id' (up to 3; not a form that is in many emails), from the to-do,
    its prepared step and its emails. Each is hashed with the Family's secret before it leaves."""
    ids = json.loads(card['event_ids'] or '[]')
    found, texts = [], [str(card['title'] or ''), str(card['body'] or '')]
    step = str(card['next_action'] or '') if 'next_action' in card.keys() else ''
    if ids:
        for event in db.execute(f"SELECT kind,body,metadata FROM events WHERE deleted=0 AND id IN ({','.join('?' * len(ids))}) "
                                'ORDER BY occurred_at DESC', tuple(ids)):
            if event['kind'] == 'gmail.message':
                message_id = str(json.loads(event['metadata'] or '{}').get('message-id') or '').strip().strip('<>').lower()
                if message_id:
                    found.append(message_id)
            texts.append(str(event['body'] or '')[:20000])
    bill = bill_of('\n'.join(texts))
    forms = [f for f in forms_of('\n'.join(texts + [step])) if _spread(db, f) <= FORM_SPREAD][:3]
    return list(dict.fromkeys(found))[:5] + (['bill:' + bill] if bill else []) + ['form:' + f for f in forms]


def found(done_by, card_id, name, member, ref, holder):
    """Note in done_by that this member did card_id (as /claims says when), the latest one winning."""
    at = str(holder.get('at') or '')[:25]
    if card_id not in done_by or at > done_by[card_id]['at']:
        done_by[card_id] = {'name': name or '', 'member_id': member['member_id'], 'fleet': ref, 'at': at}


def _load(value):
    try:
        found = json.loads(value or 'null')
    except (ValueError, TypeError):
        return None
    return found if isinstance(found, dict) else None


def line(current, done):
    """An open to-do's new done_elsewhere (JSON or None) for what this round found (done, or None), or SAME. Still
    needed (kept) keeps it quiet while that member's to-do stays done; reopened, it clears, so a later Done shows again."""
    current = _load(current)
    if done:
        if current and current.get('kept') and current.get('member_id') == done['member_id']:
            return SAME
        value = {k: done[k] for k in ('name', 'member_id', 'fleet', 'at')}
        return SAME if current == value else json.dumps(value)
    return None if current else SAME


def kept(current):
    """Still needed: the line as kept (JSON), or None when there is none."""
    current = _load(current)
    return json.dumps({**current, 'kept': True}) if current else None
