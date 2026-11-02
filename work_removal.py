"""Removing a company's work data from this Machine, when its owner leaves (or is removed from) that company's Work
Fleet and keeps their Machine. The control plane asks for it: a hosted Machine through its agent, a self-hosted one
through the Network (fleet.py, /removals). Personal sources stay.

What goes:
- the accounts whose address is at one of the company's email domains (alex@acme.com, also @eu.acme.com);
- the accounts in that company's boundary (work:Acme, matched to the Fleet's name or a company domain) that have no
  address elsewhere: the company Slack, Intercom, Salesflare or GitHub org;
- the accounts the owner marked Work for that company themselves (onboarding.set_boundary), whatever their address;
  one they marked Personal never goes;
- what they brought in: their messages and events, the cards and drafts made only from those, the promises, graph
  entries, search entries and sync state that came from them, and their own secrets when no other account uses them;
- their own sign-ins on this Machine: a Google one in gog's keyring, an Outlook one's token file. Never a sign-in an
  account that stays uses.

First a copy of config.json and the database goes into work-removal-backups/ next to the database (private, removed
after BACKUP_DAYS), so a mistake can be undone. The accounts leave config.json, then their data goes, then the
service restarts; on its start it deletes once more what a sync finishing in between may still have stored (settle).
"""
import contextlib
import datetime as dt
import json
import os
import re
import shutil
import sqlite3
import time
from pathlib import Path

import sources

BACKUP_DAYS = 7
PENDING = 'work-removal-pending.json'
CORE_CREDENTIALS = {'api-token', 'owner-token', 'gog-password', 'fleet', 'network', 'openai', 'anthropic'}


def _norm(text):
    return re.sub(r'[^a-z0-9]', '', str(text or '').casefold())


def _clean_domains(domains):
    out = []
    for d in domains or []:
        d = str(d or '').strip().lower().lstrip('@')
        if re.fullmatch(r'[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)+', d) and d not in out:
            out.append(d)
    return out


def _addresses(account):
    found = [account.get('email'), account.get('handle'), *(account.get('owner_emails') or [])]
    return [str(a).strip().lower() for a in found if isinstance(a, str) and '@' in a]


def _at(address, domains):
    host = address.rsplit('@', 1)[-1]
    return any(host == d or host.endswith('.' + d) for d in domains)


def _named(name, names):
    """A boundary's company name is the Fleet's company: the same, or one holds the other (Acme, Acme HQ)."""
    name = _norm(name)
    return bool(name) and any(name == n or (min(len(name), len(n)) >= 4 and (n in name or name in n)) for n in names)


def marked(account):
    """The owner marked this sign-in Work (with its company) or Personal themselves (onboarding.set_boundary)."""
    return account.get('boundary_by') == 'owner'


def matching(config, domains=(), companies=()):
    """The accounts to remove: [(account, why)], why 'marked', 'address' or 'boundary'. The owner's own marking comes
    first: one they marked Work for this company goes, one they marked Personal (or another company) stays, whatever
    its address. Unmarked: an account at the company's domains goes; one in the company's boundary goes when it has no
    address elsewhere (someone's personal Gmail filed under work stays)."""
    domains = _clean_domains(domains)
    names = {_norm(c) for c in companies or [] if _norm(c)} | {_norm(d.split('.')[0]) for d in domains}
    names.discard('')
    accounts = [a for a in config.get('accounts', []) if isinstance(a, dict) and a.get('id')]
    at_company = [a for a in accounts if any(_at(e, domains) for e in _addresses(a))]
    # The company's boundaries: the work ones its addresses are in (not one the owner marked as another company's),
    # and the ones named like it (Acme, Acme HQ)
    boundaries = {str(a.get('boundary')) for a in at_company if str(a.get('boundary') or '').startswith('work:') and not marked(a)}
    boundaries |= {str(a.get('boundary')) for a in accounts if str(a.get('boundary') or '').startswith('work:')
                   and _named(str(a['boundary']).split(':', 1)[1], names)}
    out = []
    for a in accounts:
        if marked(a):
            if str(a.get('boundary') or '') in boundaries:
                out.append((a, 'marked'))
        elif a in at_company:
            out.append((a, 'address'))
        elif str(a.get('boundary') or '') in boundaries and all(_at(e, domains) for e in _addresses(a)):
            out.append((a, 'boundary'))
    return out


def _data_dir(config):
    return Path(config['database']).expanduser().parent


def prune(config, days=BACKUP_DAYS):
    """Backups older than `days` go: they hold the removed company's data."""
    root = _data_dir(config) / 'work-removal-backups'
    if not root.is_dir():
        return 0
    gone = 0
    for folder in root.iterdir():
        if folder.is_dir() and not folder.is_symlink() and time.time() - folder.stat().st_mtime > days * 86400:
            shutil.rmtree(folder, ignore_errors=True)
            gone += 1
    return gone


def backup(config_path, config):
    """A private copy of config.json and the database (with its sealing key), before anything changes."""
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    root = _data_dir(config) / 'work-removal-backups'
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(root, 0o700)
    folder = root / stamp
    folder.mkdir(mode=0o700, exist_ok=True)
    shutil.copy2(config_path, folder / 'config.json')
    db_path = Path(config['database']).expanduser()
    if db_path.is_file():
        with contextlib.closing(sqlite3.connect(db_path, timeout=60)) as source, \
                contextlib.closing(sqlite3.connect(folder / db_path.name)) as target:
            source.backup(target)  # a consistent copy while the service keeps writing
        import message_seal
        key = message_seal.key_path(db_path)
        if Path(key).is_file() and not message_seal.held_elsewhere(db_path):  # a hosted key stays off the disk
            shutil.copy2(key, folder / Path(key).name)
    for item in folder.iterdir():
        os.chmod(item, 0o600)
    return folder


def _store(config):
    from assistant import Store
    return Store(config['database'], protect=config.get('message_protection'))


def _ids(value):
    try:
        found = json.loads(value or '[]')
    except ValueError:
        return []
    return found if isinstance(found, list) else []


def purge(config, account_ids, store=None):
    """Deletes what these accounts brought in. Returns counts: events, cards, drafts, graph."""
    account_ids = sorted(set(account_ids))
    counts = {'events': 0, 'cards': 0, 'drafts': 0, 'graph': 0}
    if not account_ids or not Path(config['database']).expanduser().is_file():
        return counts
    store = store or _store(config)
    gone_accounts = set(account_ids)
    with store.connect() as db:
        db.execute('PRAGMA secure_delete=ON')  # nothing deleted stays readable in a free page
        db.execute('BEGIN IMMEDIATE')
        tables = {r[0]: {c[1] for c in db.execute(f'PRAGMA table_info("{r[0]}")')}
                  for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND sql NOT LIKE 'CREATE VIRTUAL%' "
                                      "AND name NOT LIKE 'event_search%' AND name NOT LIKE 'sqlite_%'")}
        events = {r[0] for r in db.execute('SELECT id FROM events WHERE account_id IN (SELECT value FROM json_each(?))', (json.dumps(account_ids),))}
        cards = set()
        for r in db.execute('SELECT id,event_ids,account_ids FROM suggestions'):
            accounts, linked = set(map(str, _ids(r['account_ids']))), {_int(i) for i in _ids(r['event_ids'])}
            if (linked and linked <= events) or (not linked and accounts and accounts <= gone_accounts):
                cards.add(r['id'])  # made only from them; a card that also used a personal source stays
        decisions = set()
        if cards:
            decisions = {r[0] for r in _chunks(db, 'SELECT id FROM decisions WHERE suggestion_id IN ({})', cards)}
        for name in ('action_jobs', 'draft_edits'):
            if name in tables and cards:
                counts['drafts'] += sum(r[0] for r in _chunks(db, f'SELECT COUNT(*) FROM {name} WHERE suggestion_id IN ({{}})', cards))
        if 'graph_nodes' in tables:
            counts['graph'] = db.execute('SELECT COUNT(*) FROM graph_nodes').fetchone()[0]
        # Everything linked to them, by its column: rows from those accounts, events, cards and decisions on those cards
        for table in sorted(tables):
            columns = tables[table]
            if table in ('events', 'suggestions', 'decisions', 'analyses'):
                continue
            for column, values in (('decision_id', decisions), ('suggestion_id', cards), ('event_id', events), ('account_id', gone_accounts)):
                if column in columns and values:
                    # table: a name sqlite_master lists, quoted as an identifier; column: one of the four fixed names above
                    _chunks(db, 'DELETE FROM "' + table.replace('"', '""') + '" WHERE ' + column + ' IN ({})', values)
        if 'decisions' in tables and cards:
            _chunks(db, 'DELETE FROM decisions WHERE suggestion_id IN ({})', cards)
        if cards:
            _chunks(db, 'DELETE FROM suggestions WHERE id IN ({})', cards)
        if events:
            # Old review receipts keep their ids (no text), marked like other evidence the owner took out
            for review in db.execute('SELECT id,items FROM analyses').fetchall():
                items = _ids(review['items'])
                if any(isinstance(i, dict) and i.get('id') in events for i in items):
                    for i in items:
                        if isinstance(i, dict) and i.get('id') in events:
                            i['excluded'] = 'work_removed'
                    db.execute('UPDATE analyses SET items=? WHERE id=?', (json.dumps(items, separators=(',', ':')), review['id']))
            _chunks(db, 'DELETE FROM events WHERE id IN ({})', events)
        db.execute('COMMIT')
        counts['events'], counts['cards'] = len(events), len(cards)
    if 'graph_nodes' in tables:
        before = counts['graph']
        try:
            import graph
            with store.connect() as db:
                db.isolation_level = None  # graph.build runs its own transaction
                graph.build(db, config, dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'))
                counts['graph'] = max(0, before - db.execute('SELECT COUNT(*) FROM graph_nodes').fetchone()[0])
        except Exception:  # noqa: BLE001 - the graph is rebuilt again on the service's next round
            counts['graph'] = 0
    return counts


def _int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return value


def _chunks(db, sql, values, size=500):
    values, out = list(values), []
    for i in range(0, len(values), size):
        part = values[i:i + size]
        out += db.execute(sql.format(','.join('?' * len(part))), part).fetchall()
    return out


def _credential(account):
    name = account.get('credential')
    if not name and account.get('transport') == 'graph' and account.get('email'):
        import ms_graph
        name = ms_graph.credential_name(account['email'])  # an Outlook sign-in with this install's own app
    return name


def _drop_secrets(config, removed, unlink=True):
    """A removed account's own secret (its credential: also an Outlook sign-in's token file), when no account that
    stays uses it."""
    kept = {_credential(a) for a in config.get('accounts', [])}
    dropped = []
    for account in removed:
        name = _credential(account)
        if not name or name in kept or name in CORE_CREDENTIALS or name not in (config.get('credentials') or {}):
            continue
        path = Path(str(config['credentials'].pop(name))).expanduser()
        if unlink:
            for item in (path, Path(str(path) + '.lock')):
                with contextlib.suppress(OSError):
                    item.unlink()
        dropped.append(name)
    return dropped


def _forget_google(config, removed, run=None):
    """A removed account's Google sign-in in gog's keyring (gog auth remove), when no account that stays signs in with
    the same address and client. Only these: a sign-in that stays is never touched. Returns how many went."""
    import subprocess
    run = run or subprocess.run
    kept = {(str(a.get('email') or '').lower(), a.get('client')) for a in config.get('accounts', []) if a.get('transport') == 'gog'}
    gone = 0
    for key in dict.fromkeys((str(a.get('email') or '').lower(), a.get('client')) for a in removed if a.get('transport') == 'gog'):
        if '@' not in key[0] or key in kept:
            continue
        account = {'email': key[0], 'client': key[1] or ''}
        try:
            env = {**os.environ, 'GOG_KEYRING_BACKEND': 'file', 'GOG_KEYRING_PASSWORD': sources.credential(config, 'gog-password')}
            env.pop('DBUS_SESSION_BUS_ADDRESS', None)
            done = run([config.get('gog') or 'gog', 'auth', 'remove', key[0], *(['--client', key[1]] if key[1] else []), '--force', '--no-input'],
                       env=env, capture_output=True, text=True, timeout=60).returncode == 0
        except Exception:  # noqa: BLE001 - no gog, no keyring password: the token file goes below
            done = False
        try:
            path = sources.gog_token_path(config, account)
            if path.is_file():
                path.unlink()
                done = True
        except Exception:  # noqa: BLE001
            pass
        gone += done
    return gone


def remove(config_path, domains=(), companies=(), restart=None, store=None, run=None):
    """The whole removal: backup, accounts out of config.json with their own sign-ins (gog keyring, Outlook token
    file; personal ones stay), their data deleted, a note for settle, then restart() (when given). Returns
    {accounts: [{id, service, email}], events, cards, drafts, graph, secrets, signins, backup, kept_days}."""
    import onboarding
    config_path = Path(config_path)
    config = onboarding.load(config_path)
    prune(config)
    found = [a for a, _ in matching(config, domains, companies)]
    out = {'accounts': [{'id': a['id'], 'service': a.get('service', 'gmail'), 'email': (_addresses(a) or [''])[0]} for a in found],
           'events': 0, 'cards': 0, 'drafts': 0, 'graph': 0, 'secrets': 0, 'signins': 0}
    if not found:
        return out
    folder = backup(config_path, config)
    ids = [a['id'] for a in found]
    config['accounts'] = [a for a in config['accounts'] if a.get('id') not in ids]
    # Record cleanup before configuration changes: a restart can finish after any later interruption.
    note = _data_dir(config) / PENDING
    previous = json.loads(note.read_text()) if note.is_file() else {}
    credentials = dict(config.get('credentials') or {})
    pending = {'accounts': sorted(set(previous.get('accounts', [])) | set(ids)), 'at': time.time(),
               'removed': [*previous.get('removed', []), *found],
               'credentials': {**previous.get('credentials', {}), **credentials}}
    onboarding.write_private(note, json.dumps(pending))
    # The recovery note must survive a power loss before configuration changes or secret removal.
    with note.open('rb') as handle:
        os.fsync(handle.fileno())
    if os.name != 'nt':
        fd = os.open(note.parent, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    out['secrets'] = len(_drop_secrets(config, found, unlink=False))
    onboarding.save(config_path, config)
    # Never remove a credential file before the configuration that stops using it was saved.
    _drop_secrets({**config, 'credentials': credentials}, found)
    outlook = {_credential(a) for a in found if a.get('transport') == 'graph'} - {_credential(k) for k in config['accounts']}
    out['signins'] = _forget_google(config, found, run) + len(outlook - {None})
    Path(config_path).with_name(config_path.name + '.bak').unlink(missing_ok=True)  # it still lists them
    out.update(purge(config, ids, store))
    out.update(backup=folder.name, kept_days=BACKUP_DAYS)
    if restart:
        restart()
    return out


def settle(config, store=None):
    """At the service's start: what a sync finishing during a removal still stored goes too. Once."""
    try:
        note = _data_dir(config) / PENDING
        if not note.is_file():
            return None
        pending = json.loads(note.read_text())
        ids = [i for i in pending.get('accounts', []) if isinstance(i, str)]
        ids = [i for i in ids if i not in {a.get('id') for a in config.get('accounts', [])}]
        removed = [a for a in pending.get('removed', []) if isinstance(a, dict) and a.get('id') in ids]
        if removed:
            _drop_secrets({**config, 'credentials': {**pending.get('credentials', {}), **(config.get('credentials') or {})}}, removed)
            _forget_google(config, removed)
        result = purge(config, ids, store) if ids else None
        note.unlink(missing_ok=True)
        return result
    except (OSError, ValueError, sqlite3.Error):
        return None
