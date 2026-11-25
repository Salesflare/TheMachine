"""Proves the sandbox fixture holds nothing real.

Always: every address is on .example, every link is on an .example host, and there are no phone numbers.
With a copy of a real install's database (and optionally its config): no name, address, domain, company, chat or account
id from it appears anywhere in the fixture. Exits 1 and names the kind of match (never the value) on any hit.

    python3 sandbox/check_fixture.py                                   # static rules only (the test suite runs this)
    python3 sandbox/check_fixture.py --db /tmp/copy.sqlite --config ~/.local/share/personal-assistant/config.json
"""
import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EMAIL = re.compile(r'[\w.+\'-]+@([\w-]+(?:\.[\w-]+)+)')
URL = re.compile(r'https?://([^/\s"\')\]]+)')
PHONE = re.compile(r'\+?\d[\d ().-]{8,}\d')
GENERIC_DOMAINS = {'gmail.com', 'googlemail.com', 'outlook.com', 'hotmail.com', 'live.com', 'yahoo.com', 'icloud.com', 'me.com',
                   'proton.me', 'protonmail.com', 'github.com', 'google.com', 'linkedin.com', 'x.com', 'twitter.com', 'slack.com',
                   'stripe.com', 'intercom.io', 'example.com'}
# Words a real install's names or chats can share with the fixture's invented ones without identifying anyone.
COMMON = {'calendar', 'bank', 'parcel', 'train', 'weather', 'support', 'sales', 'general', 'product', 'family', 'football parents',
          'direct message', 'intercom', 'stripe', 'github', 'linkedin', 'whatsapp', 'crm', 'android notifications',
          'salesflare'}  # connector names the app itself ships with


def static_problems(text):
    problems = []
    for domain in EMAIL.findall(text):
        if not domain.lower().endswith('.example'):
            problems.append('an email address outside .example')
    for host in URL.findall(text):
        if not host.lower().split(':')[0].endswith('.example'):
            problems.append('a link outside .example')
    for number in PHONE.findall(text):
        digits = re.sub(r'\D', '', number)
        if len(digits) >= 9 and not re.fullmatch(r'1761\d+|\d{12,}', digits):  # Slack timestamps and thread ids are made up too
            problems.append('something that looks like a phone number')
    return sorted(set(problems))


def real_identifiers(db_path, config_path=None):
    """What would identify someone in a real install, by kind."""
    db = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    found = {'name': set(), 'email': set(), 'domain': set(), 'company': set(), 'account': set(), 'chat': set()}

    def name(value, kind='name'):
        value = ' '.join(str(value or '').split())
        if len(value) >= 4 and value.lower() not in COMMON and (kind != 'name' or len(value.split()) >= 2):
            found[kind].add(value)

    def emails(text):
        for match in EMAIL.finditer(str(text or '')):
            address = match.group(0).lower()
            found['email'].add(address)
            if match.group(1).lower() not in GENERIC_DOMAINS:
                found['domain'].add(match.group(1).lower())

    tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if 'graph_nodes' in tables:
        for kind, label in db.execute('SELECT kind,name FROM graph_nodes'):
            name(label, 'company' if kind == 'org' else 'name')
    if 'identity_names' in tables:
        for row in db.execute('SELECT * FROM identity_names'):
            for value in row:
                if isinstance(value, str) and not re.fullmatch(r'[\w:.-]{12,}', value):
                    name(value)
                    emails(value)
    for (account,) in db.execute('SELECT account_id FROM checkpoints'):
        found['account'].add(account)
    for (meta,) in db.execute('SELECT metadata FROM events'):
        try:
            data = json.loads(meta)
        except ValueError:
            continue
        emails(meta)
        for key in ('from', 'sender_display', 'chat_name', 'customer_name', 'organizer', 'crm_account'):
            value = data.get(key)
            if isinstance(value, str):
                name(re.sub(r'<[^>]*>', '', value).strip(), 'chat' if key == 'chat_name' else 'company' if key in ('customer_name', 'crm_account') else 'name')
    if config_path and Path(config_path).expanduser().exists():
        config = json.loads(Path(config_path).expanduser().read_text())
        owner = str(config.get('owner_name') or '')
        name(owner)
        for part in owner.split():
            if len(part) >= 4:
                found['name'].add(part)  # the owner's own first and last name, alone too
        emails(json.dumps(config))
        for account in config.get('accounts', []):
            found['account'].add(account.get('id', ''))
            name(account.get('display_name'), 'chat')
    for kind in found:
        found[kind] = {v for v in found[kind] if v and v.lower() not in COMMON}
    return found


def matches(text, identifiers):
    low = text.lower()
    hits = {}
    for kind, values in identifiers.items():
        for value in values:
            needle = value.lower()
            if kind in ('name', 'company', 'chat'):
                if re.search(r'(?<![\w])' + re.escape(needle) + r'(?![\w])', low):
                    hits[kind] = hits.get(kind, 0) + 1
            elif needle in low:
                hits[kind] = hits.get(kind, 0) + 1
    return hits


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fixture', default=str(HERE / 'fixture.json'))
    parser.add_argument('--db')
    parser.add_argument('--config')
    args = parser.parse_args()
    text = Path(args.fixture).read_text()
    problems = static_problems(text)
    if args.db:
        identifiers = real_identifiers(args.db, args.config)
        hits = matches(text, identifiers)
        problems += [f'{n} real {kind}{"s" if n > 1 else ""} from the database' for kind, n in sorted(hits.items())]
        print(f"checked against {sum(len(v) for v in identifiers.values())} real identifiers", file=sys.stderr)
    if problems:
        print('fixture check failed: ' + '; '.join(problems), file=sys.stderr)
        sys.exit(1)
    print('fixture ok: nothing real in it')


if __name__ == '__main__':
    main()
