"""The owner's own name, for what greets them (the dashboard's hello, the digests) and for signing: the one place it is
looked up. `owner_name` in config.json wins; a Machine set up without it takes the "- Name:" line of USER.md, else the
name in its title ("# USER.md - About Sam"), and a greeting the name the owner's own work mailbox gives them (Gmail's
send-as list, kept by own_addresses, or the From of their stored sent mail). '' when none of them reads as a person's. A
company, a brand or a mailbox's name ("info") never does. Read-only: neither file is written.
Who someone in a message is (own_addresses, graph, facts) is not decided with this: that keeps to `owner_name`."""
import collections
import json
import os
import re
import sqlite3
import time
import unicodedata
from pathlib import Path

from machine.config import WORKSPACE

LAYER = 1  # the owner's name, from the config and USER.md

NAME_CHARS = 80
READ_CHARS = 4000  # as OpenClaw's chats read of USER.md: the starter's Name line is its first
FIRST = re.compile(r"[^\W\d_][\w'’-]*")
# The line as the starter writes it, and as OpenClaw's own template does ("- **Name:** Sam")
NAME_LINE = re.compile(r'^[-*] +\*{0,2}Name(?::\*{0,2}|\*{0,2}:)[ \t]*(.*)$', re.I)
ABOUT_TITLE = re.compile(r'(?i)(?:USER\.md\s*[-–—:]\s*)?About\s+(.+)')
ABOUT = re.compile(r'(?i)^(?:about|who i am)\b')  # below a smaller heading, only in a section about them
# A mailbox's name more than one person reads, or a word that stands for a name: none is a first name
NOT_NAMES = frozenset('''info support hello hi team sales billing admin office contact help account accounts finance jobs careers
    legal security privacy feedback marketing partners success service orders invoices ops operations engineering product founders
    everyone staff general enquiries inquiries reception bookings events community media noreply no-reply mail post shop store
    webmaster postmaster me my you your the this that our us it owner user name unknown none not todo tbd file document notes profile
    preferences assistant agent family home life work company business machine openclaw'''.split())
LEGAL = frozenset('inc ltd llc llp bv nv bvba vzw gmbh srl sarl plc corp limited company'.split())

SENT_LOOKED_AT, MAIL_LOOKED_AT = 40, 2000  # the newest sent messages the From name comes from, among this many of the mailbox
LOOK_AGAIN = 3600  # seconds until a mailbox without a name is read again

_kept = {}  # USER.md's path: ((mtime, size), the names in it)
_mail = {}  # (database, account, address): (the mailbox's name, when it was looked for)


def first_name(name):
    """The first name in a name, or '' when it doesn't look like a person's: an address, a company ("Acme BV"), what a
    mailbox is called ("info", "Support Team")."""
    words = str(name or '').split()
    if not words or not FIRST.fullmatch(words[0]) or words[0].casefold() in NOT_NAMES:
        return ''
    return '' if len(words) > 1 and words[-1].casefold().replace('.', '') in LEGAL else words[0]


def user_md(config):
    return Path((config or {}).get('openclaw_workspace') or WORKSPACE) / 'USER.md'


def name_line(text):
    """The owner's name on USER.md's Name line, or '': the first one under a main heading (or a section about them),
    never one in a section about someone else."""
    section = ''
    for line in re.sub(r'(?s)<!--.*?-->', '', text).splitlines():
        heading = re.match(r'(#+)\s+(.*)', line)
        if heading:
            section = '' if len(heading[1]) == 1 or ABOUT.match(heading[2]) else heading[2]
        found = None if section else NAME_LINE.match(line.strip())
        if found:
            return ' '.join(found[1].split())[:NAME_CHARS]
    return ''


def capitalized(word):
    """Whether a word is written as a name's: "Rivera", "D'Arcy", "O."; not "CEO", "Sam's" or "lives"."""
    return bool(FIRST.fullmatch(word)) and not word[0].islower() and not (len(word) > 1 and word.isupper()) and not word.endswith(("'s", '’s'))


def about_name(text):
    """The owner's name in USER.md's own title ("# USER.md - About Sam", "# About Sam Rivera"), or '': its first main
    heading, or the one after OpenClaw's. The line under "About Sam" gives the full name when it starts with it and one
    to three more capitalized words ("Sam Rivera (born …"); else the first name alone."""
    lines = [line.strip() for line in re.sub(r'(?s)<!--.*?-->', '', text).splitlines()]
    for n, line in enumerate(lines):
        if not re.match(r'#\s', line):
            continue
        title = line[1:].strip()
        found = ABOUT_TITLE.match(title)
        if not found:
            if title.startswith('USER.md'):
                continue
            return ''
        words = re.split(r'\s+[-–—|]\s+|\s*[(,:]', found[1])[0].strip(' *_.').split()
        if not 1 <= len(words) <= 4 or not all(map(capitalized, words)):
            return ''
        if len(words) > 1:
            return ' '.join(words)[:NAME_CHARS]
        under = next((x for x in lines[n + 1:] if x), '').lstrip('*_->  ')
        more = re.match(re.escape(words[0]) + r"((?: [^\W\d_][\w'’-]*)+)", under.replace('*', ''))
        rest = more[1].split() if more else []
        take = next((i for i, w in enumerate(rest) if not capitalized(w)), len(rest))
        return ' '.join(words + rest[:take] if 1 <= take <= 3 else words)[:NAME_CHARS]
    return ''


def noted(config):
    """The names the owner's USER.md gives them: its Name line's and its title's. Read again only once the file
    changed: a status poll costs one stat."""
    path = user_md(config)
    try:
        stat = os.stat(path)
        mark = (stat.st_mtime_ns, stat.st_size)
        kept = _kept.get(str(path))
        if not kept or kept[0] != mark:
            with open(path, encoding='utf-8') as file:
                text = file.read(READ_CHARS)
            kept = _kept[str(path)] = (mark, tuple(n for n in (name_line(text), about_name(text)) if n))
    except (OSError, ValueError):
        return ()
    return kept[1]


def squash(text):
    folded = unicodedata.normalize('NFKD', str(text or '')).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]', '', folded.casefold())


def _parts(address):
    """(local part, the name in its domain), both plain; that name is '' for a mail provider's domain, both for what is
    no address (an X account's "@samrivera" is their own handle, never a company's domain)."""
    from graph import FREEMAIL
    local, _, domain = str(address or '').strip().lower().partition('@')
    if not local or '.' not in domain:
        return '', ''
    return local, '' if domain in FREEMAIL else squash(domain.split('.')[0])


def companies(config):
    """{what the owner's companies are called, plain: the local parts of the owner's addresses there}: from their own
    accounts' mail domains and Work names."""
    out = {}
    for account in (config or {}).get('accounts') or ():
        if not isinstance(account, dict):
            continue
        local, label = _parts(account.get('email'))
        side, _, named = str(account.get('boundary') or '').partition(':')
        for name in {label, squash(named) if side == 'work' else ''} - {''}:
            out.setdefault(name, set()).add(local)
    return out


def company(name, config):
    """Whether a name is one of the owner's companies' ("Acme", "Acme Support" at acme.example). Someone's own full name
    as their domain is not one: "Sam Rivera" at sam@samrivera.example."""
    found, first, whole = companies(config), squash(name.split()[0]), squash(name)
    return first in found or (whole in found and first not in found[whole])


def carried(name, local, label):
    """Whether a name is a person's full one that their own work address carries (sam@, sam.rivera@, srivera@), so a brand
    or a shared mailbox's name is none."""
    words = [squash(w) for w in name.split()]
    if len(words) < 2 or not all(words) or not first_name(name) or any(w in label for w in words if len(w) > 1):
        return False
    first, last = words[0], ''.join(words[1:])
    return squash(local) in (first, first + last, first[0] + last, first + last[0], last + first)


def listed_name(db, account_id, address):
    """The name a mailbox's kept send-as list gives its own address ('' mostly: Gmail fills that from the Google account)."""
    row = db.execute('SELECT entries FROM own_address_fetched WHERE account_id=?', (account_id,)).fetchone()
    entries = json.loads(row[0]) if row and row[0] else []
    return next((' '.join(str(e.get('name') or '').split()) for e in entries if isinstance(e, dict) and e.get('primary') is True
                 and e.get('address') == address), '') if isinstance(entries, list) else ''


def sent_name(db, account_id, address):
    """The name the owner's newest sent mail in this mailbox goes out under from this address, the most common one, as
    the stored messages say it: their From and labels are never sealed, nothing is asked of a provider."""
    from graph import addresses, person_name
    names = collections.Counter()
    for r in db.execute("SELECT json_extract(metadata,'$.from') FROM (SELECT metadata FROM events WHERE account_id=? AND kind='gmail.message' AND "
                        "deleted=0 ORDER BY occurred_at DESC LIMIT ?) WHERE instr(metadata,'\"SENT\"')>0 LIMIT ?", (account_id, MAIL_LOOKED_AT, SENT_LOOKED_AT)):
        for name, sender in addresses(r[0])[:1]:
            if sender == address and name:
                names[' '.join(person_name(name).split())] += 1
    return names.most_common(1)[0][0] if names else ''


def mailbox_name(config, db):
    """The name the owner's own work mailbox gives them, or '': from its send-as list, else its sent mail (carried).
    Never from a mail provider's address, where a shop's reads the same as a person's (acmebakery@gmail.com). Once found
    it is kept while this runs; none found is looked for again after LOOK_AGAIN, never on each status poll."""
    for account in (config or {}).get('accounts') or ():
        local, label = _parts(account.get('email')) if isinstance(account, dict) and not account.get('shared') else ('', '')
        if not local or not label:
            continue
        address = str(account['email']).strip().lower()
        try:
            key = (str(db.execute('PRAGMA database_list').fetchone()[2]), account.get('id'), address)
            found, looked = _mail.get(key) or ('', None)
            if not found and (looked is None or time.monotonic() - looked >= LOOK_AGAIN):
                for look in (listed_name, sent_name):
                    try:
                        name = look(db, account.get('id'), address)[:NAME_CHARS]
                    except (sqlite3.Error, ValueError, TypeError):  # a new database without that table, odd JSON
                        continue
                    if carried(name, local, label):
                        found = name
                        break
                _mail[key] = (found, time.monotonic())
        except sqlite3.Error:
            continue
        if found:
            return found
    return ''


def full_name(config, db=None):
    """The owner's name: owner_name, else USER.md's, else (with db) their mailbox's; the first that reads as a
    person's. An owner_name that doesn't stays what it is when nothing else does, as whoever set it meant it."""
    said = ' '.join(str((config or {}).get('owner_name') or '').split())
    if first_name(said):
        return said
    for name in noted(config):
        if first_name(name) and not company(name, config):
            return name
    return (mailbox_name(config, db) if db is not None else '') or said


def for_greeting(config, db=None):
    """Their first name as a greeting says it, or ''."""
    return first_name(full_name(config, db))
