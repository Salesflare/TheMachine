"""Who sent a mail, for the Graph (graph.py): an address that is a system's, never a person (bulk, relay), mail a
program sent (automated), the unsubscribes a mail app sends, and the addresses in a header. Moved out of graph.py as
is; graph.py imports these names, so graph.bulk and graph.relay still work."""
import email.utils
import functools
import re

AUTOMATED_PRECEDENCE = frozenset({'bulk', 'junk', 'list'})  # automated: mail a program sent

BULK = re.compile(r'(?:^|[._+-])(?:no[._-]?reply|do[._-]?not[._-]?reply|notifications?|notify|newsletters?|news|mailer-daemon|mailer|bounces?|postmaster|'
                  r'marketing|digest|alerts?|automated|receipts?|invoices?|billing|notetaker)(?:[._+-]|@)|@(?:[\w-]+\.)*(?:mcsv\.net|mcdlv\.net|'
                  r'sendgrid\.net|amazonses\.com|mailgun\.org|bounces?\.[\w.-]+|calendar\.google\.com|resource\.calendar\.google\.com)$'
                  r'|^(?:gemini|meet|calendar|drive|docs|forms|workspace)[\w.+-]*@google\.com$', re.I)  # Gemini's notes, Meet, Drive shares


def addresses(value):
    if isinstance(value, list):
        value = ', '.join(map(str, value))
    return list(_addresses(str(value or '')))


@functools.lru_cache(maxsize=32768)
def _addresses(text):
    """Parsed once per header: a build reads the same From and To lines thousands of times."""
    return tuple((name.strip().strip('"'), addr.strip().lower()) for name, addr in email.utils.getaddresses([text]) if '@' in addr)


def bulk(address):
    return bool(BULK.search(address))


def automated(m):
    """Mail a program sent, not a person: Precedence bulk, junk or list (Gmail's out-of-office reply is "bulk"), or
    Auto-Submitted. The owner's own auto-reply goes to the address the mail came back from, often a bounce address
    (pm_bounces@pm-bounces.example.com): sent from the owner's mailbox, yet nobody they wrote to."""
    return str(m.get('precedence') or '').lower() in AUTOMATED_PRECEDENCE or bool(m.get('auto_submitted'))


# System and relay addresses: never a person, also not when the owner wrote to one (a reply through Intercom goes to a
# relay). Intercom's Operator bot and its reply relays, GitHub's noreply and reply addresses, reply+token relays of
# feedback and ticket tools, and the notification senders of Slack, Google Calendar and GitHub.
RELAY = re.compile(r'^operator\+[^@]*@intercom\.io$|@(?:[\w-]+\.)*intercom-mail\.(?:com|eu|io)$'
                   r'|@(?:[\w-]+\.)*(?:no-?reply|reply)\.github\.com$|@(?:[\w-]+\.)*no-?reply\.[\w-]+(?:\.[\w-]+)+$'
                   r'|^(?:reply|replies)[+=][^@]+@'
                   r'|(?:^|[._+-])(?:no[._-]?reply|do[._-]?not[._-]?reply|notifications?)(?:[._+-]|@)'
                   r'|^(?:calendar-notification|calendar-server|notify|feedback|bot)@(?:[\w-]+\.)*(?:google|slack|github)\.com$'
                   # A return path a mailing system makes per message: the recipient written into it (VERP:
                   # bounces+sam=acme.com@), a signed bounce tag (BATV: prvs=, msprvs1=) or a message id (Amazon SES)
                   r'|^[^@]*[+-][^@=]*=[a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,}@|^(?:prvs|msprvs\d*|btv\d*)='
                   r'|^0[0-9a-f]{15}-[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}-0{6}@', re.I)


def list_unsubscribes(db, signals, owner):
    """Event ids of the unsubscribes the owner's mail app sent for them: a new mail (no reply) from the owner to one
    address, with "unsubscribe" as its whole subject, as a list's List-Unsubscribe link asks. It goes to an address
    made for that one list and recipient (unsub-4cca9a1c.z83o@bnc3.mail.example): nobody they wrote to. Only those
    few mails' subjects are read."""
    ids = [e for e, _, kind, _, m in signals if kind == 'gmail.message' and not m.get('in-reply-to') and not m.get('cc')
           and ('SENT' in (m.get('labels') or ()) or any(owner.mine(a) for _, a in addresses(m.get('from'))[:1]))
           and len(addresses(m.get('to'))) == 1]
    found = set()
    for start in range(0, len(ids), 500):
        chunk = ids[start:start + 500]
        found |= {r[0] for r in db.execute(f"SELECT id,title FROM events WHERE id IN ({','.join('?' * len(chunk))})", chunk)
                  if str(r[1] or '').strip().casefold() == 'unsubscribe'}
    return found


def relay(address):
    """A system or relay address: never a person, whoever wrote to it."""
    return bool(RELAY.search(str(address or '').lower()))
