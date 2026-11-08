"""Who sent a mail, for the Graph (graph.py): an address that is a system's, never a person (bulk, relay), mail a
program sent (automated), the unsubscribes a mail app sends, a mailing's sender (mass_mail, unless the owner's word or
work is on them: owner_kept), and the addresses in a header. graph.py imports these names, so graph.bulk and
graph.relay still work."""
import email.utils
import functools
import json
import re
import sqlite3

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


# A name written like a person's: "Jane Doe", "Peeters Lieve", "PEETERS Lieve". Not one word ("Paperbox"), not
# shouted whole ("ALIEXPRESS DEALS"), no digits.
NAME_WORD = re.compile(r"[^\W\d_](?:[^\W\d_]|['’.-](?=[^\W\d_]))*\.?")


def person_shaped(name):
    words = str(name or '').split()
    return 2 <= len(words) <= 3 and all(NAME_WORD.fullmatch(w) and w[0].isupper() for w in words) and not all(w.isupper() for w in words)


def mass_mail(m, sender, name, company, wrote_to):
    """Why a mail is one a mailing system sent in a sender's name, not a person writing to the owner, else '':
    'list' (List-Unsubscribe or List-Id), 'reply_to' (replies asked to go to another address, unless a person's name
    sent it as a plain mail: no bulk address, nothing automated) or 'company' (their company's name, the one the
    address's domain spells, is the whole display name: "Paperbox" at paperbox.example, never a person's name like "Jane Doe" at
    janedoe.com; company is what graph.org_from_name read from it). Never once the owner wrote to them, and never a
    reply. sender: the From address; any other is no sender of this mail."""
    if sender in wrote_to or m.get('in-reply-to') or [a for _, a in addresses(m.get('from'))[:1]] != [sender]:
        return ''
    if m.get('list_unsubscribe') or m.get('list_id'):
        return 'list'
    replies = [a for _, a in addresses(m.get('reply-to'))]
    if replies and sender not in replies and not (person_shaped(name) and not bulk(sender) and not automated(m)):
        return 'reply_to'
    folded = lambda text: ' '.join(str(text or '').casefold().split())
    return 'company' if company and folded(company) == folded(name) and not person_shaped(name) else ''


# What the owner said or keeps on someone: they stay a person whatever their mail looks like. person_facts is left out:
# enrichment fills it for anyone.
KEPT = ('SELECT identifier FROM person_roles', 'SELECT identifier FROM person_edits', 'SELECT node_id FROM graph_names',
        'SELECT identifier FROM manual_nodes', 'SELECT identifier FROM contact_marks', 'SELECT node_id FROM record_owners',
        'SELECT a FROM graph_merges UNION SELECT b FROM graph_merges', 'SELECT a FROM graph_relations UNION SELECT b FROM graph_relations',
        'SELECT event_id FROM promises', 'SELECT identifier FROM mail_shown',
        'SELECT j.value FROM suggestions s, json_each(s.event_ids) j')


def owner_kept(db):
    """Identifiers and event ids the owner's word or work is on (a role, an edit, a name, a note, a merge, an owner, a
    promise or a to-do): a mailing that carries one still counts its sender."""
    found = set()
    for sql in KEPT:
        try:
            found |= {r[0] for r in db.execute(sql)}
        except sqlite3.OperationalError:
            pass  # a table this database doesn't have yet
    return found


# The senders the last build left out as mailings (mail_hidden), and the ones the owner showed as a person (mail_shown):
# those never are again.
SCHEMA = ('''CREATE TABLE IF NOT EXISTS mail_hidden(identifier TEXT PRIMARY KEY,name TEXT,why TEXT NOT NULL,mails INTEGER NOT NULL,last_at TEXT)''',
          '''CREATE TABLE IF NOT EXISTS mail_shown(identifier TEXT PRIMARY KEY,created_at TEXT NOT NULL)''')


def ensure(db):
    for sql in SCHEMA:
        db.execute(sql)


class Hidden:
    """What one build leaves out: {identifier: [name, why, mails, last_at, strength]}, the latest mail's name and
    reason. The strength fades like a person's (half_life days), and one faded below floor would be nobody anyway."""

    def __init__(self, now, half_life, floor):
        self.now, self.half_life, self.floor, self.found = now, half_life, floor, {}

    def add(self, found, why, at):
        """found: the mail's touches, its sender first. Returns the rest."""
        row = self.found.setdefault(found[0][0], [found[0][1], why, 0, '', 0.0])
        row[2] += 1
        row[4] += found[0][2] * 0.5 ** (max(0.0, (self.now - at).total_seconds() / 86400) / self.half_life)
        if at.isoformat() >= row[3]:
            row[0], row[1], row[3] = found[0][1] or row[0], why, at.isoformat()
        return found[1:]

    def publish(self, db, nodes):
        """Keep the list of the ones nobody's a person by: another mail (or the owner) may have made them one anyway."""
        people = set()
        for n in nodes:
            info = n[9] if isinstance(n[9], dict) else json.loads(n[9] or '{}')
            people |= {n[0], *(info.get('identifiers') or ())}
        db.execute('DELETE FROM mail_hidden')
        db.executemany('INSERT INTO mail_hidden(identifier,name,why,mails,last_at) VALUES(?,?,?,?,?)',
                       [(i, *row[:4]) for i, row in self.found.items() if i not in people and row[4] >= self.floor])


def hidden_count(db):
    try:
        return db.execute('SELECT COUNT(*) FROM mail_hidden').fetchone()[0]
    except sqlite3.OperationalError:
        return 0


def hidden_page(db, cursor=0, limit=30):
    """Hidden senders, the latest first, a page at a time."""
    offset, limit = max(0, int(cursor or 0)), max(1, min(int(limit), 50))
    rows = db.execute('SELECT identifier,name,why,mails,last_at FROM mail_hidden ORDER BY last_at DESC,identifier LIMIT ? OFFSET ?',
                      (limit + 1, offset)).fetchall()
    items = [{'id': r[0], 'address': r[0].removeprefix('email:'), 'name': r[1] or r[0].removeprefix('email:'), 'why': r[2], 'mails': r[3],
              'last_at': r[4]} for r in rows[:limit]]
    return {'items': items, 'next': str(offset + limit) if len(rows) > limit else None, 'total': hidden_count(db)}


def show(db, identifier, now):
    """The owner's "Show as a person": their mail counts from the next build on, whatever it looks like."""
    identifier = str(identifier or '').strip().lower()
    if not identifier.startswith('email:') or '@' not in identifier:
        raise ValueError('identifier is a hidden sender, email:<address>')
    db.execute('INSERT OR IGNORE INTO mail_shown(identifier,created_at) VALUES(?,?)', (identifier, now))
    db.execute('DELETE FROM mail_hidden WHERE identifier=?', (identifier,))
    return {'identifier': identifier, 'shown': True}
