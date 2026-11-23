"""The owner's own name, for what greets them (the dashboard's hello, the digests) and for signing: the one place it is
looked up. `owner_name` in config.json wins; a Machine set up without it takes the "- Name:" line of USER.md, and a
greeting the name the owner's own work mailbox gives them (Gmail's send-as list, kept by own_addresses). '' when none of
them reads as a person's. A company, a brand or a mailbox's name ("info") never does. Read-only: neither file is written.
Who someone in a message is (own_addresses, graph, facts) is not decided with this: that keeps to `owner_name`."""
import json
import os
import re
import sqlite3
import unicodedata
from pathlib import Path

from machine.config import WORKSPACE

LAYER = 1  # the owner's name, from the config and USER.md

NAME_CHARS = 80
READ_CHARS = 4000  # as OpenClaw's chats read of USER.md: the starter's Name line is its first
FIRST = re.compile(r"[^\W\d_][\w'’-]*")
# The line as the starter writes it, and as OpenClaw's own template does ("- **Name:** Sam")
NAME_LINE = re.compile(r'^[-*] +\*{0,2}Name(?::\*{0,2}|\*{0,2}:)[ \t]*(.*)$', re.I)
ABOUT = re.compile(r'(?i)^(?:about|who i am)\b')  # below a smaller heading, only in a section about them
# A mailbox's name more than one person reads, or a word that stands for a name: none is a first name
NOT_NAMES = frozenset('''info support hello hi team sales billing admin office contact help account accounts finance jobs careers
    legal security privacy feedback marketing partners success service orders invoices ops operations engineering product founders
    everyone staff general enquiries inquiries reception bookings events community media noreply no-reply mail post shop store
    webmaster postmaster me my you your the owner user name unknown none not todo tbd'''.split())
LEGAL = frozenset('inc ltd llc llp bv nv bvba vzw gmbh srl sarl plc corp limited company'.split())

_kept = {}  # USER.md's path: ((mtime, size), its Name line)


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


def noted(config):
    """name_line of the owner's USER.md, read again only once the file changed: a status poll costs one stat."""
    path = user_md(config)
    try:
        stat = os.stat(path)
        mark = (stat.st_mtime_ns, stat.st_size)
        kept = _kept.get(str(path))
        if not kept or kept[0] != mark:
            with open(path, encoding='utf-8') as file:
                kept = (mark, name_line(file.read(READ_CHARS)))
            _kept[str(path)] = kept
    except (OSError, ValueError):
        return ''
    return kept[1]


def squash(text):
    folded = unicodedata.normalize('NFKD', str(text or '')).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]', '', folded.casefold())


def _parts(address):
    """(local part, the name in its domain), both plain; that name is '' for a mail provider's domain."""
    from graph import FREEMAIL
    local, _, domain = str(address or '').strip().lower().partition('@')
    return local, '' if not domain or domain in FREEMAIL else squash(domain.split('.')[0])


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


def mailbox_name(config, db):
    """The name the owner's own work mailbox gives them, as its kept send-as list says it, or '': a full name that the
    address itself carries (sam@, sam.rivera@, srivera@), so a brand or a shared mailbox's name is none. Never from a
    mail provider's address, where a shop's reads the same as a person's (acmebakery@gmail.com)."""
    for account in (config or {}).get('accounts') or ():
        local, label = _parts(account.get('email')) if isinstance(account, dict) and not account.get('shared') else ('', '')
        if not local or not label:
            continue
        try:
            row = db.execute('SELECT entries FROM own_address_fetched WHERE account_id=?', (account.get('id'),)).fetchone()
            entries = json.loads(row[0]) if row and row[0] else []
        except (sqlite3.Error, ValueError, TypeError):
            continue
        for entry in entries if isinstance(entries, list) else ():
            if not isinstance(entry, dict) or entry.get('primary') is not True or entry.get('address') != str(account['email']).strip().lower():
                continue
            name = ' '.join(str(entry.get('name') or '').split())[:NAME_CHARS]
            words = [squash(w) for w in name.split()]
            if len(words) < 2 or not all(words) or not first_name(name) or any(w in label for w in words if len(w) > 1):
                continue
            first, last = words[0], ''.join(words[1:])
            if squash(local) in (first, first + last, first[0] + last, first + last[0], last + first):
                return name
    return ''


def full_name(config, db=None):
    """The owner's name: owner_name, else USER.md's, else (with db) their mailbox's; the first that reads as a
    person's. An owner_name that doesn't stays what it is when nothing else does, as whoever set it meant it."""
    said = ' '.join(str((config or {}).get('owner_name') or '').split())
    if first_name(said):
        return said
    name = noted(config)
    if first_name(name) and not company(name, config):
        return name
    return (mailbox_name(config, db) if db is not None else '') or said


def for_greeting(config, db=None):
    """Their first name as a greeting says it, or ''."""
    return first_name(full_name(config, db))
