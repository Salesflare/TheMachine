"""Whether a mail's sender address is really the sender's: the owner's own mail service checked it (DMARC, or a DKIM signature
of the address's own domain) and wrote so in the message's Authentication-Results. A display name never counts, nor does a
header the sender added: only the topmost one is the receiving service's. A mailbox whose service isn't known to write it
(IMAP) verifies nothing."""
from __future__ import annotations

import email.utils
import re

KEY = 'verified_sender'  # in a stored message's metadata: True, or absent
RESULT = re.compile(r'^\s*(?:dkim|dmarc)\s*=\s*pass\b.*?\bheader\.(?:d|i|from)\s*=\s*@?([a-z0-9.-]+)', re.I | re.S)


def verified(account, headers):
    """headers: the message's own [{'name', 'value'}], in their order."""
    found = [(str(h.get('name', '')).lower(), str(h.get('value', ''))) for h in headers or () if isinstance(h, dict)]
    results = next((v for k, v in found if k == 'authentication-results'), '')
    senders = [a for k, v in found if k == 'from' for _, a in email.utils.getaddresses([v])]
    service = account.get('service')
    if len(senders) != 1 or '@' not in senders[0] or service == 'imap' or service != 'outlook' and not results.strip().lower().startswith('mx.google.com;'):
        return False
    domain = senders[0].rpartition('@')[2].lower().rstrip('.')
    plain = re.sub(r'"(?:[^"\\]|\\.)*"', '', results)  # what a sender can put words in: a quoted part or a comment
    while (cut := re.sub(r'\([^()]*\)', ' ', plain)) != plain:
        plain = cut
    for part in plain.split(';'):
        if m := RESULT.match(part):
            signed = m[1].lower().rstrip('.')
            if '.' in signed and (signed == domain or domain.endswith('.' + signed) or signed.endswith('.' + domain)):
                return True
    return False
