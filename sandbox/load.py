"""Builds a sandbox install from the fixture: a config, credentials and a database in one directory, in one of
several states. Nothing here is real; the config points at no real service and turns every sender off.

    python3 sandbox/load.py --dir /tmp/machine-sandbox --state busy

States (combine with commas, e.g. fleet,friends):
    fresh        just installed: two accounts, the first signals, no cards and no review yet
    reviews-off  a normal install with reviews switched off
    busy         a full day: every source, open and prepared cards, promises, decisions, reviews
    fleet        busy, in a work Fleet with three teammates (one without a Machine), their questions and a seat request
    friends      busy, with two friends, a request in and one out
    family       busy, in a Family Fleet
    expired      busy, with the work Google sign-in expired (Gmail and Calendar)
    all          busy + fleet + friends + family

A demo Machine (the app directories' review account) is a real, freshly installed Machine with the busy day loaded
into its own database, run on it as its owner with the installed app on the path:

    python3 sandbox/load.py --machine ~/.config/the-machine/config.json [--app /path/to/installed/app]

It adds none of the fixture's mail, chat and calendar accounts and leaves the config as it is: nothing syncs, no
account exists to send from, no saved logins, no Fleet, no friends. It refuses a database that already has signals.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import secrets
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STATES = ('fresh', 'reviews-off', 'busy', 'fleet', 'friends', 'family', 'expired', 'notes', 'all')
HOST = 'machine.sandbox.example'  # the dashboard's host name; run.py's proxy sends it
EXPIRED = 'google_signin_expired_run_gog_auth_add'


def parse_states(text):
    states = {s.strip() for s in str(text or 'busy').split(',') if s.strip()}
    unknown = states - set(STATES)
    if unknown:
        raise SystemExit(f"unknown state {', '.join(sorted(unknown))}; choose from {', '.join(STATES)}")
    if 'all' in states:
        states |= {'busy', 'fleet', 'friends', 'family'}
    return states


def groups(states):
    """The Network groups this state is in: work, family, friends."""
    return [g for g, s in (('work', 'fleet'), ('family', 'family'), ('friends', 'friends')) if s in states]


try:
    from zoneinfo import ZoneInfo
    BRUSSELS = ZoneInfo('Europe/Brussels')  # the sandbox owner's timezone (config 'timezone')
except Exception:  # no tz database (Windows without tzdata): winter time is close enough for made-up meetings
    BRUSSELS = dt.timezone(dt.timedelta(hours=1))


def stamp(minutes_ago, base):
    return (base - dt.timedelta(minutes=minutes_ago)).isoformat()


def write_secret(path, value):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as handle:
        handle.write(value)


def make_config(directory, fixture, states, port, network_port):
    accounts = fixture['accounts']
    if 'fresh' in states:
        accounts = [a for a in accounts if a['id'] in ('work-gmail', 'work-calendar')]
    credentials = {}
    for name in ('api-token', 'owner-token') + (('fleet',) if groups(states) else ()):
        write_secret(directory / name, secrets.token_hex(24))
        credentials[name] = str(directory / name)
    config = {
        'owner_name': fixture['owner']['name'], 'timezone': 'Europe/Brussels', 'telegram_owner': '',
        'tailscale_owner': fixture['owner']['email'], 'dashboard_host': HOST, 'dashboard_path': '/', 'dashboard_aliases': [],
        'port': port, 'database': str(directory / 'events.sqlite'), 'credentials': credentials,
        'app_dir': str(ROOT), 'openclaw': '/nonexistent/openclaw', 'node': '/nonexistent/node', 'gog': '/nonexistent/gog', 'wacli': '/nonexistent/wacli',
        'openclaw_state': str(directory / 'openclaw.sqlite'), 'agent_db': str(directory / 'agent.sqlite'),
        'delivery_enabled': False, 'digest_at': '08:30', 'bootstrap_days': 7, 'poll_seconds': 300, 'http_timeout': 15,
        'prompt_receipts': str(directory / 'prompt-receipts'), 'attachment_dir': str(directory / 'attachments'), 'attachment_sources': [],
        'booking_links': {'30-minute call': 'https://book.example/alex/30min'},
        'review_worker': {'enabled': 'reviews-off' not in states, 'min_signals': 40, 'max_wait_minutes': 15},
        'weekly_recap': {'enabled': True}, 'embeddings': {'enabled': False}, 'enrichment': {'enabled': False},
        'accounts': accounts, 'sandbox': True, 'openclaw_config': str(directory / 'openclaw.json'),
        'browser_cdp_url': 'http://127.0.0.1:9',  # no browser: never the one on this computer (guard.py refuses it too)
    }
    # OpenClaw's own settings as the dashboard reads them (the main model and its thinking level), made up
    (directory / 'openclaw.json').write_text(json.dumps({'agents': {'defaults': {'model': {'primary': 'acme/lm-2.5-swift'}, 'thinkingDefault': 'low'}}}))
    if groups(states):
        config['fleet'] = {'url': f'http://127.0.0.1:{network_port}/api/fleet'}
    path = directory / 'config.json'
    path.write_text(json.dumps(config, indent=2))
    return config, path


def working_hours(start, duration, slot, base):
    """The same day (a weekend moves to Friday or Monday), on a round half hour between 09:00 and 18:00 in Brussels,
    so a meeting reads like one whenever the sandbox starts. `slot` picks the half hour. A Sunday that is over when the
    sandbox loads (base) moves back when Monday's hour is still to come, and a Saturday to come moves on when Friday's
    has gone: the move off the weekend never puts a meeting on the other side of now."""
    local = start.astimezone(BRUSSELS)
    latest = (18 * 60 - duration) // 30  # the last half hour it still ends by 18:00
    minutes = 9 * 60 + 30 * (slot % (latest - 18 + 1))
    on = lambda days: dt.datetime.combine(local.date() + dt.timedelta(days=days), dt.time(minutes // 60, minutes % 60), BRUSSELS).astimezone(dt.timezone.utc)
    if local.weekday() < 5:
        return on(0)
    near, other = {5: (-1, 2), 6: (1, -2)}[local.weekday()]
    return on(near) if (on(near) <= base) == (start <= base) else on(other)


def calendar_meta(meta, base):
    start = working_hours(base - dt.timedelta(minutes=meta['start_minutes_ago']), meta['duration_minutes'], meta['start_minutes_ago'], base)
    end = start + dt.timedelta(minutes=meta['duration_minutes'])
    out = {k: v for k, v in meta.items() if k not in ('start_minutes_ago', 'duration_minutes', 'attendees', 'organizer')}
    return {**out, 'start': {'dateTime': start.isoformat()}, 'end': {'dateTime': end.isoformat()}, 'end_at': end.isoformat(), 'all_day': False,
            'timezone': 'Europe/Brussels', 'organizer': {'email': meta['organizer']},
            'attendees': [{'email': a, **({'self': True} if a == meta['organizer'] else {'responseStatus': 'accepted'})} for a in meta['attendees']]}


def load(directory, states, port=8870, network_port=8871, fixture_path=HERE / 'fixture.json', base=None):
    """Writes the install into `directory` (emptied first) and returns (config, config_path). base: the moment it is
    loaded at (now by default); a fixed one loads the same install every time (tests/test_graph_golden.py)."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for name in ('events.sqlite', 'events.sqlite-wal', 'events.sqlite-shm', 'sent.jsonl'):
        (directory / name).unlink(missing_ok=True)
    fixture = json.loads(Path(fixture_path).read_text())
    config, config_path = make_config(directory, fixture, states, port, network_port)
    os.environ['HOME'] = str(directory)  # before assistant is imported: nothing of the real install is read
    sys.path.insert(0, str(ROOT))
    import assistant
    import graph

    store = assistant.Store(config['database'])
    base = base or dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    fresh = 'fresh' in states
    accounts = {a['id'] for a in config['accounts']}
    events = [e for e in fixture['events'] if e['account_id'] in accounts]
    if fresh:  # the first sync: a day of mail and the week's meetings
        events = [e for e in events if e['minutes_ago'] < 24 * 60]
    with store.connect() as db:
        ids = insert_events(db, events, base, 0 if fresh else 1)
        for account in config['accounts']:
            if 'expired' in states and account['id'] in ('work-gmail', 'work-calendar'):
                error = f"{account['service']}:{EXPIRED}"
                db.execute('INSERT INTO checkpoints(account_id,state,last_success,error,error_at,failures) VALUES(?,?,?,?,?,?)',
                           (account['id'], '{}', stamp(26 * 60, base), error, stamp(4, base), 31))
                for hours in range(0, 26, 2):
                    db.execute('INSERT INTO sync_activity VALUES(?,?,?,?,?,?,?)', (secrets.token_hex(16), account['id'], stamp(hours * 60 + 4, base), 'failed', None, error, None))
            elif account.get('signals') is False:  # action-only: no sync, only what it may do (connectors/docs.py refresh)
                db.execute('INSERT INTO checkpoints(account_id,state) VALUES(?,?)',
                           (account['id'], json.dumps({'provider': account.get('provider'), 'replies': False, 'writes': ['create']})))
            else:
                # The CRM's last round of accounts, as sync_salesflare leaves it: with no dates seen, its card counts its reads
                read = {'mode': 'incremental', 'read_from': (base - dt.timedelta(days=90)).isoformat(),  # a calendar's days read in full
                        'read_until': (base + dt.timedelta(days=30)).isoformat()} if str(account.get('service') or '').endswith('calendar') else {}
                crm = {'mode': 'incremental', 'watermark': stamp(3, base), 'inaccessible_accounts': [9001],
                       'last_round': {'at': stamp(3, base), 'accounts': 18, 'read': 17, 'no_access': 1, 'refused': 1, 'set_aside': 0}}
                db.execute('INSERT INTO checkpoints(account_id,state,last_success,last_sync_signals) VALUES(?,?,?,?)',
                           (account['id'], json.dumps(crm if account.get('service') == 'salesflare' else read), stamp(3, base),
                            sum(1 for e in events if e['account_id'] == account['id'])))
                db.execute('INSERT INTO sync_activity VALUES(?,?,?,?,?,?,?)', (secrets.token_hex(16), account['id'], stamp(3, base), 'success', 2, None, None))
        if not fresh:
            load_cards(db, fixture, ids, base)
            load_reviews(db, ids, base, assistant, fixture)
            load_boards(db, fixture, ids, base)
            load_companies(db, fixture, base)
            load_history(db, base)
    if not fresh:
        with store.connect() as db:
            load_job(db, fixture, base)
            db.commit()  # graph.build opens its own transaction
            graph.build(db, config, base.isoformat())
            load_roles(db, base)
            load_learned(db, base)
            load_fields(db, base)
            load_trips(db, base)
            load_briefing(db, base)
            load_skills(db, states, fixture, base)
            # The owner's first view after setup (Store.greeting): the hello by name, leading with who waits longest
            assistant.Store.greeting_on(db, base.isoformat())
            if 'fleet' in states:
                load_share(db)
                load_owners(db, fixture, base)
        load_logins(directory, fixture)
        if not fresh:
            load_learned_facts(store)
            load_home_facts(store, base)
        load_recurring(store, config, base)
        if not fresh:  # a fresh Machine has no routines yet: the page's empty state
            load_routines(store, base)
        if 'notes' in states:  # never part of `all`: the site's demo is recorded from `all` and shows no notes to bring in
            load_notes(store, config, directory)
        if not fresh:  # a fresh Machine has no profile yet
            load_profile('notes' in states)
    return config, config_path


def insert_events(db, events, base, analyzed=1):
    """The fixture's signals into the open Store connection (sealed, when its database is); returns {key: event id}."""
    ids = {}
    for e in events:
        meta = calendar_meta(e['metadata'], base) if e['kind'] == 'calendar.event' else e['metadata']
        body = e['body']
        if meta.get('photo_fixture'):  # a WhatsApp photo, read (whatsapp_images.py): kept here as the Machine keeps it
            body, meta = load_photo(db, e, meta, base)
        at = meta['start']['dateTime'] if e['kind'] == 'calendar.event' else stamp(e['minutes_ago'], base)
        db.execute('INSERT INTO events(account_id,source_id,kind,occurred_at,title,body,metadata,deleted,content_hash,version,analyzed_version,ingested_at) '
                   'VALUES(?,?,?,?,?,?,?,0,?,1,?,?)',
                   (e['account_id'], 'sandbox:' + e['key'], e['kind'], at, e['title'], body, json.dumps(meta),
                    hashlib.sha256((e['title'] + body).encode()).hexdigest(), analyzed, stamp(max(e['minutes_ago'], 0) - 1, base)))
        ids[e['key']] = db.execute('SELECT last_insert_rowid()').fetchone()[0]
    return ids


def load_photo(db, e, meta, base):
    """A made-up photo the Machine kept and read for one WhatsApp message, with Read photos on for its connection
    (personal chats too): its file next to the database (sealed when the database is), its row, and the message's text
    and metadata as whatsapp_images.with_photo makes them. Returns (body, metadata)."""
    import whatsapp_images
    meta = dict(meta)
    photo = meta.pop('photo_fixture')
    database = next(r[2] for r in db.execute('PRAGMA database_list') if r[1] == 'main')
    at = stamp(e['minutes_ago'], base)
    row = whatsapp_images.add_read(db, {'database': database}, e['account_id'], 'sandbox:' + e['key'], meta['chat_id'], meta['message_id'],
                                   (HERE / photo['file']).read_bytes(), photo['description'], photo['text'], at,
                                   'wp_' + hashlib.sha256(e['key'].encode()).hexdigest()[:20])
    whatsapp_images.set_prefs(db, e['account_id'], True, True, at)
    made = whatsapp_images.with_photo({'body': e['body'], 'metadata': meta}, row)
    return made['body'], made['metadata']


def fill_machine(config, fixture_path=HERE / 'fixture.json', base=None):
    """The busy day into a real Machine's own database (config['database']), through its Store, with none of the
    fixture's accounts added. Returns how many signals, to-dos and promises it holds."""
    import assistant
    import graph

    # Every Machine has its own OpenClaw gateway as an account (its chat channel, with no bot of its own here)
    if any(a.get('service') != 'gateway' for a in config.get('accounts', [])):
        raise SystemExit('This Machine has accounts connected: a demo Machine starts with none.')
    fixture = json.loads(Path(fixture_path).read_text())
    store = assistant.Store(config['database'])
    base = base or dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    with store.connect() as db:
        if db.execute('SELECT 1 FROM events LIMIT 1').fetchone():
            raise SystemExit('This Machine already has signals: a demo Machine starts empty.')
        ids = insert_events(db, fixture['events'], base)
        load_cards(db, fixture, ids, base)
        load_reviews(db, ids, base, assistant, fixture)
        load_boards(db, fixture, ids, base)
        load_companies(db, fixture, base)
    with store.connect() as db:
        load_job(db, fixture, base)
        db.commit()  # graph.build opens its own transaction
        # The Graph is built as if the made-up accounts were there (which side each person is on); they are not saved
        graph.build(db, {**config, 'accounts': fixture['accounts']}, base.isoformat())
        load_roles(db, base)
        load_fields(db, base)
        load_skills(db, {'busy'}, fixture, base)
        counts = [db.execute(f'SELECT count(*) FROM {t}').fetchone()[0] for t in ('events', 'suggestions', 'promises')]
    return dict(zip(('signals', 'todos', 'promises'), counts))


def load_history(db, base):
    """How far back each connection's history reaches (machine/store/history.py): mail and calendars a year, done, and
    WhatsApp still coming in, so its card says so far. Only the cards' and the Calendar's lines; no older rows."""
    from machine.store import history
    year, upper = stamp(365 * 24 * 60, base), stamp(8 * 24 * 60, base)
    for account, kept, oldest, done in (('work-gmail', 4180, year, True), ('home-gmail', 1260, year, True), ('work-calendar', 610, year, True),
                                        ('home-calendar', 140, year, True), ('home-whatsapp', 2930, stamp(190 * 24 * 60, base), False)):
        history.save(db, account, {'target': year, 'upper': upper, 'cursor': oldest}, stamp(30, base), kept, oldest, done, history.DEFAULT_DAYS)


def load_recurring(store, config, base):
    """A to-do that repeats (recurring.py): the weekly numbers, every Monday, made the way New to-do makes one, with the way
    it is done kept for the next one."""
    import recurring
    account = next((a['id'] for a in config['accounts'] if str(a.get('boundary') or '').startswith('work:')), None)
    if not account:
        return
    today = base.date()
    monday = today + dt.timedelta(days=(7 - today.weekday()) % 7)
    saved = store.owner_card('Send the team the weekly numbers', account, work=True, due=monday.isoformat())
    with store.connect() as db:
        card = db.execute('SELECT * FROM suggestions WHERE id=?', (saved['id'],)).fetchone()
        recurring.start(db, card, {'unit': 'week', 'n': 1}, monday, card['owner_words'] or card['title'], base.isoformat(), work=True)
        # how it's done, kept from an earlier week for the next one (recurring.save_method): its chat shows Edit and Undo
        recurring.save_method(db, card['id'], '1. Take signups, revenue and churn for last Monday to Sunday from the metrics board.\n'
                              '2. Compare each with the week before.\n3. Draft one short Slack message to the team channel; you send it.', base.isoformat())


def sandbox_jobs(monday, today):
    """Old OpenClaw jobs: (job id, name, words, rule, anchor, at, 'on' or 'suggested', the preview's result)."""
    return [('sandbox-job-0001', 'Weekly Intercom', 'Sum up this week’s support issues and improvement requests', {'unit': 'week', 'n': 1}, monday, '12:00',
             'on', '**Duplicate reminders** came up in 4 conversations, all on the mobile app.\n**Export to Excel** asked for 3 times.'),
            ('sandbox-job-0002', 'Failed payments', 'List customers whose payment failed, with the amount and since when', {'unit': 'week', 'n': 1}, monday, '09:15',
             'suggested', '**Halyard**: card declined twice, **€480** open since Tuesday.\n**Brightpath Logistics**: card expired, renews Friday.'),
            ('sandbox-job-0003', 'Call prep', 'Prep me for today’s customer calls: who, what they last asked and what is open', {'unit': 'weekday', 'n': 1}, today, '07:00',
             'suggested', '**Northwind Analytics** at 10:00 with Mila: they compare annual pricing for 25 seats.\n**Gullwing Clinics** at 15:00: '
             'the onboarding plan they asked for is still open.')]


def load_routines(store, base):
    """Routines (routines.py): two that ran a few times, as the Routines page shows them after a couple of weeks; one
    from an old OpenClaw job that ran well for a week (Turn off the old job?), two suggestions from OpenClaw jobs and one
    from mail the owner forwards by hand."""
    import routines
    now = base.replace(tzinfo=None)
    today = now.date()
    monday = today - dt.timedelta(days=today.weekday())
    with store.connect() as db:
        deals = routines.create(db, 'Sum up my open deals: what moved last week, what went quiet and what needs me',
                                {'unit': 'week', 'n': 1}, monday, '09:00', now, stamp(20 * 24 * 60, base))
        replies = routines.create(db, 'List the emails I still owe a reply, oldest first', {'unit': 'weekday', 'n': 1}, today, '08:00',
                                  now, stamp(10 * 24 * 60, base))
        runs = [(deals, 14, 'ready', '**Fernwave** moved to proposal; the pilot starts in two weeks.\n**Halyard** went quiet after the '
                 'sync delay: no reply in 9 days.\nNeeds you: **Gullwing Clinics** asks for the onboarding plan by Friday.', None),
                (deals, 7, 'ready', '**Fernwave** asked for references.\nNothing new on **Halyard**.', None),
                (replies, 1, 'nothing', None, 'No new emails waiting for a reply since yesterday'),
                (replies, 2, 'failed', None, 'usage_limited')]
        for routine_id, days, state, result, why in runs:
            run_id = routines.begin(db, routine_id, (today - dt.timedelta(days=days)).isoformat(), stamp(days * 24 * 60, base))
            routines.finish(db, run_id, state, stamp(days * 24 * 60 - 3, base), result=result,
                            why=why if state == 'nothing' else None, error=why if state == 'failed' else None)
        for job_id, name, words, rule, anchor, at, state, result in sandbox_jobs(monday, today):
            rid = routines.create(db, words, rule, anchor, at, now, stamp(12 * 24 * 60, base), name=name, origin='openclaw:' + job_id,
                                  state='sorting')
            run_id = routines.begin(db, rid, 'sort:' + stamp(11 * 24 * 60, base), stamp(11 * 24 * 60, base))
            routines.sorted_as(db, run_id, 'routine', stamp(11 * 24 * 60 - 5, base), name=name, instructions=words, text=result)
            if state == 'on':  # added 10 days ago; three good runs since
                routines.accept(db, rid, now, stamp(10 * 24 * 60, base))
                for days in (9, 5, 2):
                    run_id = routines.begin(db, rid, (today - dt.timedelta(days=days)).isoformat(), stamp(days * 24 * 60, base))
                    routines.finish(db, run_id, 'ready' if days == 2 else 'nothing', stamp(days * 24 * 60 - 3, base),
                                    result=result if days == 2 else None, why=None if days == 2 else 'Nothing new this week')
        # one from what the owner does by hand (routine_patterns.py): school and club mails forwarded to Robin one by one
        friday = today + dt.timedelta(days=(4 - today.weekday()) % 7)
        why = {'kind': 'forward', 'n': 6, 'weeks': 3, 'to': 'Robin'}
        rid = routines.create(db, 'Sort a pattern: Forwards to Robin', {'unit': 'week', 'n': 1}, friday, '08:00', now, stamp(3 * 24 * 60, base),
                              name='Forwards to Robin', origin='pattern:forward:sandbox', state='sorting', why=why)
        run_id = routines.begin(db, rid, 'sort:' + stamp(3 * 24 * 60, base), stamp(3 * 24 * 60, base))
        routines.sorted_as(db, run_id, 'routine', stamp(3 * 24 * 60 - 4, base), name='School digest',
                           instructions='Every Friday, sum up the week’s school and swim club mails for Robin',
                           text='**School trip** on Thursday: packed lunch and a rain jacket.\n- Swim club: no training next Tuesday\n'
                                '- Parent evening sign-up closes Monday')
        db.commit()


def load_openclaw_jobs(config):
    """The old OpenClaw jobs the routines above came from, still on (routine_imports.py reads them read-only), so the
    page asks to turn the old job off. Only for a served sandbox (run.py): an export would take this file as data."""
    today = dt.date.today()
    with closing(sqlite3.connect(config['openclaw_state'])) as claw, claw:
        claw.execute('CREATE TABLE IF NOT EXISTS cron_jobs(job_id TEXT PRIMARY KEY,name TEXT,description TEXT,enabled INTEGER,'
                     'payload_kind TEXT,job_json TEXT,sort_order INTEGER)')
        claw.executemany('INSERT OR IGNORE INTO cron_jobs(job_id,name,enabled,payload_kind,job_json,sort_order) VALUES(?,?,1,?,?,?)',
                         [(j[0], j[1], 'agentTurn', json.dumps({'schedule': {'kind': 'cron', 'expr': '0 9 * * 1'}, 'payload': {'message': j[2]}}), i)
                          for i, j in enumerate(sandbox_jobs(today, today))])


def load_owners(db, fixture, base):
    """Graph: a few projects owned by a teammate, picked by hand (crm.set_owner), so boards and Mine show the split."""
    import crm
    team = fixture['network']['work']['team']
    for name, m in (('Gullwing Clinics onboarding', 0), ('Halyard sync delay', 1), ('Fernwave', 2)):
        row = db.execute('SELECT id FROM projects WHERE name=?', (name,)).fetchone()
        if row:
            crm.set_owner(db, f'project:{row[0]}', team[m]['member_id'], team[m]['name'], stamp(2 * 24 * 60, base))
    db.commit()


def load_fields(db, base):
    """Graph: two organization fields and a few tags (crm_fields.py), as someone running it like a CRM would add."""
    import crm_fields
    when = stamp(3 * 24 * 60, base)
    plan = crm_fields.save_field(db, {'kind': 'org', 'name': 'Plan', 'type': 'choice', 'choices': 'Starter\nGrowth\nEnterprise'}, when)
    seats = crm_fields.save_field(db, {'kind': 'org', 'name': 'Seats', 'type': 'number'}, when)
    for domain, tier, count, tags in (('meridianrobotics.example', 'Enterprise', '120', ('Partner',)),
                                      ('harborlinehealth.example', 'Growth', '40', ('Pilot',)),
                                      ('northwindanalytics.example', None, None, ('Partner',))):
        node = f'org:{domain}'
        if not db.execute('SELECT 1 FROM graph_nodes WHERE id=?', (node,)).fetchone():
            continue
        if tier:
            crm_fields.set_value(db, node, plan['id'], tier, when)
            crm_fields.set_value(db, node, seats['id'], count, when)
        for label in tags:
            crm_fields.tag(db, node, label, now=when)
    db.commit()


def load_trips(db, base):
    """Trips and events in Calendar (note_pages.py): a trip The Machine keeps from booking mail and events from ticket
    mail, so their bands and their pages show something."""
    import note_pages
    when, day = stamp(2 * 24 * 60, base), lambda days: (base + dt.timedelta(days=days)).date().isoformat()
    work = 'work:Lumen Labs'
    # A trip from booking mail (trip_notes.py): the flights', the hotel's, the train's and the taxi's confirmations, with
    # the structured data the mail source reads or the model reads (bookings.py), and a show's tickets during it, made
    # into one trip under Trips as the Machine's ten-minute step does; nothing is booked from the airport to the hotel
    import trip_notes
    air = lambda number, dep, arr, at, until: {'type': 'flight', 'code': 'K7PQ2M', 'status': 'confirmed', 'start': at, 'end': until,
                                                'from': dep, 'to': arr, 'number': 'LX ' + number, 'by': 'Skylink Air'}
    mails = [('trip:flights', 'Your flights to Lisbon', 'booking@skylink-air.example', 'Skylink Air', 2 * 24 * 60,
              [{**air('2084', 'Brussels', 'Lisbon', day(18) + 'T07:10', day(18) + 'T08:55'), 'seat': '14A'},
               air('2087', 'Lisbon', 'Brussels', day(21) + 'T18:45', day(21) + 'T22:20')]),
             ('trip:hotel', 'Booking confirmed: Hotel Alfama Garden', 'stay@alfama-garden.example', 'Hotel Alfama Garden', 30 * 60,
              [{'type': 'hotel', 'code': 'AG-55190', 'status': 'confirmed', 'start': day(18) + 'T15:00', 'end': day(21) + 'T11:00',
                'name': 'Hotel Alfama Garden', 'where': 'Lisbon', 'address': 'Rua de São Miguel 12, Lisbon', 'guests': '1'}]),
             ('trip:train', 'Your e-ticket: Antwerp to Brussels Airport', 'tickets@rail.example', 'Example Rail', 26 * 60,
              [{'type': 'train', 'code': 'RX-30418', 'status': 'confirmed', 'start': day(18) + 'T05:12', 'end': day(18) + 'T05:49',
                'from': 'Antwerp', 'to': 'Brussels Airport', 'number': 'IC 3510', 'seat': '42', 'read': 'text'}]),
             ('trip:taxi', 'Ride booked: hotel to Lisbon airport', 'rides@cabs.example', 'Example Cabs', 20 * 60,
              [{'type': 'taxi', 'code': 'LT-7731', 'status': 'confirmed', 'start': day(21) + 'T16:30', 'from': 'Hotel Alfama Garden',
                'to': 'Lisbon Airport', 'read': 'text'}]),
             ('trip:show', 'Your tickets: Fado night at Casa Azul', 'tickets@fado.example', 'Casa Azul', 18 * 60,
              [{'type': 'event', 'code': 'FD-118', 'status': 'confirmed', 'start': day(19) + 'T21:00', 'name': 'Fado night',
                'where': 'Casa Azul, Lisbon', 'guests': '2', 'read': 'text'}])]
    insert_events(db, [{'key': key, 'account_id': 'work-gmail', 'kind': 'gmail.message', 'minutes_ago': minutes, 'title': subject,
                        'body': f'Thank you for booking with {name}. Your booking code and details are below.',
                        'metadata': {'from': f'{name} <{sender}>', 'to': 'alex@lumenlabs.example', 'labels': ['INBOX'], 'thread_id': 't-' + key.replace(':', '-'),
                                     'message-id': f'<{key.replace(":", ".")}@mail.example>', 'bookings': rows,
                                     'source_url': f'https://mail.example/#inbox/t-{key.replace(":", "-")}'}}
                       for key, subject, sender, name, minutes, rows in mails], base)
    # Events from ticket mail (event_notes.py): a concert with two orders on the personal mailbox, one with a to-do to
    # pay, and a two-day conference on the work mailbox
    import event_notes
    show = lambda code, at, until=None, **more: {'type': 'event', 'code': code, 'status': 'confirmed', 'start': at, **({'end': until} if until else {}), **more}
    concert = {'name': 'Northern Lights Live', 'where': 'Riverside Arena, Antwerp', 'by': 'Example Tickets'}
    mails = [('event:concert', 'home-gmail', 'Your tickets for Northern Lights Live', 'orders@tickets.example', 'Example Tickets', 5 * 24 * 60,
              [show('TK-4411', day(26) + 'T20:00', guests='2', seat='B 14', **concert)]),
             ('event:concert2', 'home-gmail', 'Order confirmed: Northern Lights Live', 'orders@tickets.example', 'Example Tickets', 2 * 24 * 60,
              [show('TK-5520', day(26) + 'T20:00', **concert)]),
             ('event:summit', 'work-gmail', 'Registration confirmed: Example Dev Summit', 'events@devsummit.example', 'Example Dev Summit', 9 * 24 * 60,
              [show('DS-2207', day(33) + 'T09:00', day(34) + 'T17:30', name='Example Dev Summit', where='Expo Hall, Lyon')])]
    ids = insert_events(db, [{'key': key, 'account_id': account, 'kind': 'gmail.message', 'minutes_ago': minutes, 'title': subject,
                              'body': f'Thank you for your order with {name}. Your tickets and booking code are below.',
                              'metadata': {'from': f'{name} <{sender}>', 'to': 'alex@lumenlabs.example' if account == 'work-gmail' else 'alex.morgan@mail.example',
                                           'labels': ['INBOX'], 'thread_id': 't-' + key.replace(':', '-'), 'message-id': f'<{key.replace(":", ".")}@mail.example>', 'bookings': rows,
                                           'source_url': f'https://mail.example/#inbox/t-{key.replace(":", "-")}'}}
                             for key, account, subject, sender, name, minutes, rows in mails], base)
    db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,created_at,status) VALUES(?,?,?,?,?,?,?,'completed')",
               ('5e1f0a2b3c4d5e6f', 'sandbox:event-pay', 'Pay for the Northern Lights Live tickets', 'Pay the second order before it lapses.',
                json.dumps([ids['event:concert2']]), json.dumps(['home-gmail']), stamp(2 * 24 * 60 - 30, base)))
    trip_notes.collect(db)
    accounts = [{'id': 'work-gmail', 'service': 'gmail', 'boundary': work}, {'id': 'home-gmail', 'service': 'gmail', 'boundary': 'personal'}]
    found, keep = trip_notes.drafts(db, accounts)
    note_pages.sync(db, 'trip', found, when, keep)
    found, keep = event_notes.drafts(db, accounts)
    note_pages.sync(db, 'event', found, when, keep)
    # Home's bills: paid energy and water bills on the personal mailbox, each with its done to-do
    bills =[('Brightwater Energy', days) for days in (95, 64, 33, 3)] + [('Clearbrook Water', days) for days in (150, 58)]
    mails = insert_events(db, [{'key': f'home:bill{n}', 'account_id': 'home-gmail', 'kind': 'gmail.message', 'minutes_ago': days * 24 * 60,
                                'title': f'Your {payee} bill', 'body': f'Your new bill from {payee} is ready.',
                                'metadata': {'from': f'{payee} <billing@{payee.split()[0].lower()}.example>', 'to': 'alex.morgan@mail.example',
                                             'labels': ['INBOX'], 'thread_id': f't-home-bill{n}', 'message-id': f'<home.bill{n}@mail.example>'}}
                               for n, (payee, days) in enumerate(bills)], base)
    for n, (payee, days) in enumerate(bills):
        db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at,bill) VALUES(?,?,?,?,?,?,'completed',?,?)",
                   (hashlib.sha256(f'home-bill{n}'.encode()).hexdigest()[:16], f'sandbox:home-bill{n}', f'Pay the {payee} bill', f'The {payee} bill, paid.',
                    json.dumps([mails[f'home:bill{n}']]), json.dumps(['home-gmail']), stamp(days * 24 * 60, base),
                    json.dumps({'payee': payee, 'invoice': f'HB-{4410 + n}', 'amount': 'EUR 64.20'})))
    # Health and the kids: events only the owner goes to on the personal calendar (days before now; below 0 still to
    # come) and paid bills
    me = 'alex.morgan@mail.example'
    for kind, visits, bills in (('health', (('Dentist check-up', 170), ('Dentist check-up', -20), ('GP visit', 41), ('Physio', 16),
                                            ('Physio', 9), ('Physio', 2)), (('Smileline Dental', 12), ('Northcare Health Insurance', 26))),
                                ('kids', (('Parents evening', -9), ('Hockey tournament', -12)), (('Oakfield School', 20), ('Riverside Hockey Club', 33)))):
        insert_events(db, [{'key': f'{kind}:visit{n}', 'account_id': 'home-calendar', 'kind': 'calendar.event', 'minutes_ago': max(days, 0) * 24 * 60,
                            'title': title, 'body': '', 'metadata': {'start_minutes_ago': days * 24 * 60 + n, 'duration_minutes': 45,
                                                                     'attendees': [me], 'organizer': me, 'status': 'confirmed'}}
                           for n, (title, days) in enumerate(visits)], base)
        mails = insert_events(db, [{'key': f'{kind}:bill{n}', 'account_id': 'home-gmail', 'kind': 'gmail.message', 'minutes_ago': days * 24 * 60,
                                    'title': f'Your invoice from {payee}', 'body': f'Your invoice from {payee} is ready.',
                                    'metadata': {'from': f'{payee} <billing@{payee.split()[0].lower()}.example>', 'to': me,
                                                 'labels': ['INBOX'], 'thread_id': f't-{kind}-bill{n}', 'message-id': f'<{kind}.bill{n}@mail.example>'}}
                                   for n, (payee, days) in enumerate(bills)], base)
        for n, (payee, days) in enumerate(bills):
            db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at,bill) VALUES(?,?,?,?,?,?,'completed',?,?)",
                       (hashlib.sha256(f'{kind}-bill{n}'.encode()).hexdigest()[:16], f'sandbox:{kind}-bill{n}', f'Pay the {payee} invoice',
                        f'The {payee} invoice, paid.', json.dumps([mails[f'{kind}:bill{n}']]), json.dumps(['home-gmail']), stamp(days * 24 * 60, base),
                        json.dumps({'payee': payee, 'invoice': f'{kind[0].upper()}C-{2210 + n}', 'amount': 'EUR 48.00'})))
    db.commit()


def load_home_facts(store, base):
    """A few things the owner said in their chat about the house, their health and their daughter Isla, kept the way
    the chat keeps them (Store.remember_fact)."""
    import graph
    with store.connect() as db:  # Isla, added by hand as Personal (as on a person's page), and what she is to the owner (To you)
        import crm_import
        import graph_show
        at, personal = stamp(3 * 24 * 60, base), {'side': 'personal'}
        done = graph.create_record(db, 'person', {'name': 'Isla Morgan', 'email': 'isla.morgan@mail.example'}, at)  # an address: the same node id each load
        if done.get('created'):
            crm_import.details_made(db, [done['node_id']], personal, at)
            graph_show.show_new_people(db, [done], personal)
        graph.set_role(db, done['node_id'], 'daughter', 'owner', at)
        row = (done['node_id'],)
        db.commit()
    said = ('The boiler is serviced every October by Northside Heating', 'The gutters are cleaned each November',
            'The fridge warranty runs until June 2027', 'The dishwasher is a Lumo DW-500, bought in March 2024',
            'Allergic to penicillin', 'Blood type is A positive', 'Takes vitamin D in winter', 'The autumn term ends on 18 December')
    for n, text in enumerate(said):
        store.remember_fact(text, f'webchat-said:sandbox-home-{n}', said=True, quote=text, said_text=text)
    for n, text in enumerate(('Isla is in class 4B, her teacher is Ms Okafor', 'Isla has hockey practice on Wednesdays until 5') if row else ()):
        store.remember_fact(text, f'webchat-said:sandbox-kids-{n}', said=True, quote=text, said_text=text, about=[row[0]])


def load_share(db):
    """The Shared Graph (shared_graph.py): the reviews' call on each Work email thread, as they would have made it.
    Client threads go to the team; one about something personal to the client stays private (its existence only)."""
    import shared_graph
    shared_graph.ensure(db)
    calls, sensitive = [], None
    # a few the review was unsure of, in the groups it would give them, for "Share these?"
    unsure = {'Webinar together?': ('Partner and co-marketing', 'team'), 'Partnership idea': ('Partner and co-marketing', 'team'),
              'Podcast slot next week': ('Partner and co-marketing', 'team'), 'Intro: Sunniva <> Alex': ('Intros to investors', 'people')}
    for row in db.execute("SELECT id,title,metadata FROM events WHERE account_id='work-gmail' AND kind='gmail.message' ORDER BY occurred_at DESC"):
        meta = json.loads(row['metadata'] or '{}')
        people = shared_graph.addresses(meta)
        if not people:
            continue
        if all(a.endswith('@lumenlabs.example') for a in people):
            calls.append({'event_id': row['id'], 'share': 'internal'})
            continue
        who = str(meta.get('from') or '').split('<')[0].strip().split(' ')[0] or 'They'
        title = re.sub(r'^(re|fwd?):\s*', '', str(row['title'] or ''), flags=re.I)
        if title in unsure:
            calls.append({'event_id': row['id'], 'share': 'unsure', 'group': unsure[title][0], 'suggest': unsure[title][1]})
            continue
        if sensitive is None and 'lumenlabs' not in str(meta.get('from') or ''):
            sensitive = row['id']
            calls.append({'event_id': row['id'], 'share': 'sensitive'})
            continue
        calls.append({'event_id': row['id'], 'share': 'client', 'line': f"{who} wrote about {' '.join(str(row['title'] or '').split())[:80]}"})
    shared_graph.judge(db, calls)


def load_job(db, fixture, base):
    """A card handed to Claude Code earlier, with its result: the card's job block (agent_jobs.py)."""
    import agent_jobs
    job = fixture.get('agent_job')
    if not job:
        return
    db.executescript(agent_jobs.SCHEMA)
    card_id = hashlib.sha256(job['card'].encode()).hexdigest()[:16]
    at = stamp(40, base)
    db.execute('INSERT INTO agent_jobs(id,suggestion_id,tool,place,status,brief,session_id,summary,files,turns,created_at,updated_at,started_at,finished_at) '
               'VALUES(?,?,?,?,?,?,?,?,?,1,?,?,?,?)',
               ('sandbox-job-1', card_id, job['tool'], 'local', 'result', 'Answer the question on the to-do.', 'sandbox-session', job['summary'],
                json.dumps([{'path': f} for f in job['files']]), stamp(55, base), at, stamp(54, base), at))


def load_logins(directory, fixture):
    """Connections > Sign-ins: sites the browser signs back in to. Made-up sites; the password is a placeholder."""
    import browser_login
    import message_seal
    message_seal.load_key(directory / 'events.sqlite', create=True)  # the app makes it at start too; sealed in-process, no openssl
    logins = browser_login.LoginStore(directory)
    for entry in fixture.get('saved_logins', []):
        logins.save(entry['site'], entry['username'], 'sandbox-placeholder', account=entry.get('account'))


def load_roles(db, base):
    """Roles a review read for the four closest people, on their pages and in their Recent changes."""
    import graph
    roles = [('head of operations', 'I run operations here, so send the rollout plan my way.'), ('finance lead', 'Looping in finance; I sign off on the invoice.'),
             ('product manager', 'As PM for the mobile app I own the beta list.'), ('customer success', 'I look after your account from our side.')]
    people = db.execute("SELECT id FROM graph_nodes WHERE kind='person' ORDER BY strength DESC LIMIT 4").fetchall()
    for (node_id,), (role, quote) in zip(people, roles):
        graph.set_role(db, node_id, role, 'review', base.isoformat(), quote=quote)


def load_learned(db, base):
    """A person's Recent changes (record_log.py): where they work, read in a signature; how they relate to a colleague;
    and a fact from the owner's note on a to-do that a newer note updated (the older one condensed into it)."""
    import graph

    def person(address):
        row = db.execute("SELECT n.id FROM graph_nodes n, json_each(n.info,'$.identifiers') j WHERE n.kind='person' AND j.value=?",
                         ('email:' + address,)).fetchone()
        return row[0] if row else None

    def event(title, address):
        row = db.execute("SELECT id FROM events WHERE title=? AND json_extract(metadata,'$.from') LIKE ? ORDER BY occurred_at DESC LIMIT 1",
                         (title, '%<' + address + '>')).fetchone()
        return row[0] if row else None
    who, colleague = person('thibault@meridianrobotics.example'), person('oskar@meridianrobotics.example')
    receipt = event('Receipt for INV-8061', 'thibault@meridianrobotics.example')
    if not who or not receipt:
        return
    graph.set_org(db, who, 'Meridian Robotics', 'review', stamp(60 * 50, base), event_id=receipt, quote='Accounts, Meridian Robotics')
    renewal = event('Renewal quote for Meridian Robotics', 'oskar@meridianrobotics.example')
    if colleague and renewal:
        graph.relate(db, who, colleague, 'colleague of', 'review', stamp(60 * 30, base), event_id=renewal)
    card = hashlib.sha256(b'closed10').hexdigest()[:16]  # the owner's two notes on that to-do; load_learned_facts keeps them
    db.executemany("INSERT OR IGNORE INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,'other',?,'dashboard',?)",
                   [('sandbox-note-1', card, 'The renewal is for 40 seats.', stamp(60 * 70, base)),
                    ('sandbox-note-2', card, 'They cut it to 8 seats.', stamp(60 * 6, base))])


def load_learned_facts(store):
    """A fact from the owner's note on a to-do that a newer note updated: kept the way a review keeps them
    (Store.remember_fact), the older one condensed into the newer, so the person's Recent changes says what it was."""
    with store.connect() as db:
        row = db.execute("SELECT n.id FROM graph_nodes n, json_each(n.info,'$.identifiers') j WHERE n.kind='person' AND j.value=?",
                         ('email:thibault@meridianrobotics.example',)).fetchone()
        notes = db.execute("SELECT count(*) FROM decisions WHERE id IN ('sandbox-note-1','sandbox-note-2')").fetchone()[0]
    if not row or notes != 2:
        return
    old = store.remember_fact('The Meridian Robotics renewal is for 40 seats.', 'sandbox-note-1', about=[row[0]], quote='renewal is for 40 seats')
    store.remember_fact('The Meridian Robotics renewal is now for 8 seats.', 'sandbox-note-2', replaces=[old['id']], about=[row[0]],
                        quote='They cut it to 8 seats')


NOTES = {'MEMORY.md': """# MEMORY.md

## People

- Thibault at Meridian Robotics wants every quote as a PDF, never a link.
- Ilse from the school board only reads messages after 8 pm.

## How we work

- Customer calls are never booked on Friday afternoon.
- Renewal mails always name the seat count and the renewal date in the first line.
- Tried the new note app in March, went back after a week.

## Setup

- The backup script lives in ~/bin and runs at night.
""", 'USER.md': """# About me

- Northwind Freight is our oldest customer: their mails go first.
"""}
# USER.md's profile section as the first profile writes it (onboarding.render_profile): What I've learned, Your profile
PROFILE_MD = """
## Observed from my messages
<!-- assistant profile 2026-10-12 · edit freely; delete this line to keep later drafts out -->

- Role: Runs sales and customer success at a small software company
- Tone: Short and friendly; first names; no exclamation marks
- Greeting: Hi + first name in English; Hoi in Dutch
- Sign-off: Thanks, then the first name
- Languages: English: customers and partners; Dutch: the team

### What matters
- Meridian Robotics: the renewal this quarter
- Northwind Freight: the oldest customer
"""


def load_profile(notes=False):
    """What the first profile turn wrote into USER.md, after the owner's own notes when the sandbox has them, in the
    workspace the app reads (machine.config.WORKSPACE, under the sandbox's HOME)."""
    from machine.config import WORKSPACE
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    (WORKSPACE / 'USER.md').write_text((NOTES['USER.md'] if notes else '# About me\n') + PROFILE_MD)


NOTES_PICKS = [(1, 'Thibault at Meridian Robotics wants every quote as a PDF, never a link.', 'preference'),
               (2, 'Ilse from the school board only reads messages after 8 pm.', 'fact'),
               (3, 'Customer calls are never booked on Friday afternoon.', 'preference'),
               (4, 'Renewal mails name the seat count and the renewal date in the first line.', 'rule'),
               (7, 'Northwind Freight is our oldest customer: their mails go first.', 'preference')]


def load_notes(store, config, directory):
    """Bring these in (bring_in.py): made-up OpenClaw notes in the sandbox's own workspace, read the way the daily
    pass reads them, with the judge's answer written out here (the sandbox starts no model)."""
    import bring_in
    workspace = Path(directory) / 'workspace'
    workspace.mkdir(parents=True, exist_ok=True)
    for name, text in NOTES.items():
        (workspace / name).write_text(text)
    with store.connect() as db:
        db.execute('BEGIN IMMEDIATE')
        state = bring_in.prepare(db, workspace, config)
        bring_in.conclude(db, state, json.dumps([{'n': n, 'text': text, 'kind': kind} for n, text, kind in NOTES_PICKS]))


def load_skills(db, states, fixture, base):
    """Settings > Skills: the example as the owner's own, one the Machine proposes, one it learned from a Do it task
(learned_skills.py), and in a Fleet one a teammate shared."""
    import skills
    skills.ensure(db)
    example = skills.EXAMPLES['customer-inquiries']
    rows = [('sk_sandbox_mine', example, 'on', 'mine', None, None, None),
            ('sk_sandbox_proposed', {'name': 'Prepare the weekly pipeline update',
                                     'description': 'When the owner asks for the weekly pipeline numbers for the team call.',
                                     'body': '1. Count new, won and lost deals since last Monday.\n2. List the three largest open deals with their next step.\n3. Draft five lines for the owner to post.'},
             'proposed', 'proposed', None, None, 'You asked for this four Mondays in a row.'),
            ('sk_sandbox_learned', {'name': 'Download an invoice from the supplier portal',
                                    'description': 'Use when working on portal.harborlinehealth.example: download an invoice from the supplier portal.',
                                    'body': "## Steps\n1. Sign in with the saved sign-in.\n2. Open Billing, then Statements; Invoices moved there.\n"
                                            "3. Download the PDF and attach it to the to-do.\n\n## Didn't work\n- The search box ignores invoice numbers.\n\n"
                                            "## Workarounds\n- Sort by date instead of searching.\n\n## Done when\nThe PDF is saved and its number matches the to-do."},
             'on', 'learned', None, None, None)]
    if {'fleet', 'all'} & set(states):
        team = fixture['network']['work']
        rows.append(('sk_sandbox_shared', {'name': 'Qualify an inbound demo request before the first call',
                                           'description': 'When someone books a demo through the website form.',
                                           'body': '1. Look up the company: size, industry, current tools.\n2. Check earlier conversations with anyone there.\n3. Write three questions for the call.'},
                     'incoming', 'shared', team['team'][0]['name'], team['id'], 'Saved me an hour a day on demo prep.'))
    for skill_id, s, status, origin, author, fleet_id, note in rows:
        at = stamp(60 * 24, base)
        db.execute('INSERT OR REPLACE INTO skills(id,slug,name,description,body,status,origin,version,sha,author,fleet,member_id,note,created_at,updated_at) '
                   'VALUES(?,?,?,?,?,?,?,1,?,?,?,?,?,?,?)',
                   (skill_id, skills.slug_of(s['name']), s['name'], s['description'], s['body'], status, origin,
                    skills.digest(s['name'], s['description'], s['body']), author, fleet_id,
                    fixture['network']['work']['team'][0]['member_id'] if author else None, note, at, at))


def load_briefing(db, base):
    """Tomorrow's first meeting with someone, and its briefing as a web search leaves it (meeting_prep.py)."""
    import i18n
    import meeting_prep
    ids = insert_events(db, [{'key': 'briefing:call', 'account_id': 'work-calendar', 'kind': 'calendar.event', 'minutes_ago': -1500, 'title': 'Intro call with Aldermoss',
                              'body': 'Video call with Thea Marchetti.',
                              'metadata': {'attendees': ['alex@lumenlabs.example', 'thea@aldermoss.example'], 'organizer': 'alex@lumenlabs.example', 'start_minutes_ago': -1500,
                                           'duration_minutes': 30, 'status': 'confirmed', 'source_url': 'https://calendar.example/event/aldermoss-intro'}}], base)
    event, made, key, card_id = ids['briefing:call'], stamp(50, base), meeting_prep.KEY_PREFIX + 'sandbox', 'b21ef1a2b3c4d5e6'
    start = dt.datetime.fromisoformat(db.execute('SELECT occurred_at FROM events WHERE id=?', (event,)).fetchone()[0])
    body = meeting_prep.body_text({'who': 'Thea Marchetti, head of support at Aldermoss', 'background': 'Ran support at a parcel carrier before that.',
                                   'company': 'Rents cargo bikes to shops in six cities, from €79 a month.',
                                   'bring': 'How reminders would work on their shared support inbox.'}, i18n.t,
                                  {'background': ['https://people.example/thea-marchetti'], 'company': ['https://aldermoss.example/']})
    db.execute("INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at,source_line) VALUES(?,?,?,?,?,?,'pending',?,?)",
               (card_id, key, 'Prepare for the Aldermoss intro call', body, json.dumps([event]), json.dumps(['work-calendar']), made, 'Source: your calendar'))
    db.execute('INSERT INTO deliveries(suggestion_id,status,updated_at) VALUES(?,?,?)', (card_id, 'sent', made))
    meeting_prep.keep(db, {'key': key, 'id': event, 'start': start}, 'made', card_id, made, body, searches=2)


def send_later_card(db, card, card_id, at, base):
    """Approved, and waiting for a time someone picked, on the hour (machine/store/send_later.py)."""
    from machine.store import send_later
    import next_actions
    revision = card['next_action']['revision']
    action = next_actions.selected(json.dumps(card['next_action']), revision)
    send_at = dt.datetime.fromisoformat(stamp(-card['snooze_hours'] * 60, base)).replace(minute=0, second=0, microsecond=0).isoformat()
    send_later.schedule(db, {'id': card_id}, revision, action, 'later-' + card_id, 'dashboard', None, send_at, at)


def load_cards(db, fixture, ids, base):
    import graph
    for name in fixture['projects']:
        db.execute('INSERT OR IGNORE INTO projects(name,created_at) VALUES(?,?)', (name, stamp(30 * 24 * 60, base)))
    for card in fixture['cards']:
        event_ids = [ids[k] for k in card['events'] if k in ids]
        if not event_ids:
            continue
        card_id = hashlib.sha256(card['key'].encode()).hexdigest()[:16]
        created = stamp(card['minutes_ago'], base)
        snoozed = stamp(-card['snooze_hours'] * 60, base) if card.get('snooze_hours') and not card.get('send_later') else None
        db.execute('INSERT INTO suggestions(id,dedupe_key,title,body,event_ids,account_ids,status,created_at,snoozed_until,resume_status,next_action,'
                   'urgent,source_line,project) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                   (card_id, 'sandbox:' + card['key'], card['title'], card['body'], json.dumps(event_ids), json.dumps(card['accounts']), card['status'],
                    created, snoozed, 'pending' if snoozed else None, json.dumps(card['next_action']) if card.get('next_action') else None,
                    int(bool(card.get('urgent'))), f"Source: {card['source']} · {(base - dt.timedelta(minutes=card['minutes_ago'])).strftime('%a, %b %d').replace(' 0', ' ')}",
                    card.get('project')))
        if card.get('outcome'):  # what its run said is left (Store.prepare): needs_you with nothing ready reads Needs you
            db.execute('UPDATE suggestions SET outcome=? WHERE id=?', (json.dumps(card['outcome']), card_id))
        if card.get('asks'):  # its chat's taps (Store.set_chat_asks)
            db.execute('UPDATE suggestions SET chat_asks=? WHERE id=?', (json.dumps(card['asks']), card_id))
        if card.get('done_by'):  # Already did this: a Family member closed the same to-do as done (Fleet.mark_done_elsewhere)
            family = fixture['network']['family']
            member = next(m for m in family['team'] if m['name'] == card['done_by']['name'])
            db.execute('UPDATE suggestions SET done_elsewhere=? WHERE id=?', (json.dumps(
                {'name': member['name'].split()[0], 'member_id': member['member_id'], 'fleet': family['id'],
                 'at': stamp(card['done_by']['minutes_ago'], base)}), card_id))
        if card.get('based_on') in ids:  # the teammate's input the draft follows: "Based on Priya in #sales"
            db.execute('UPDATE suggestions SET based_on=? WHERE id=?', (ids[card['based_on']], card_id))
        db.execute('INSERT INTO deliveries(suggestion_id,status,updated_at) VALUES(?,?,?)', (card_id, 'sent', created))
        if card.get('send_later'):
            send_later_card(db, card, card_id, created, base)
        if card.get('project'):  # Graph > Projects: the card's thread carries its project, as a review labels it
            graph.label(db, event_ids, card['project'], 'review', created)
        if card.get('choice'):
            db.execute('INSERT INTO decisions(id,suggestion_id,choice,feedback,source,created_at) VALUES(?,?,?,?,?,?)',
                       ('d' + card_id, card_id, card['choice'], '', 'dashboard', stamp(max(card['minutes_ago'] - 30, 1), base)))
    for p in fixture['promises']:
        if p['event'] not in ids:
            continue
        due = (base + dt.timedelta(days=p['due_days'])).date().isoformat() if p.get('due_days') is not None else None
        account = db.execute('SELECT account_id FROM events WHERE id=?', (ids[p['event']],)).fetchone()[0]
        db.execute('INSERT OR IGNORE INTO promises(direction,who,what,due,check_at,event_id,account_id,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?)',
                   (p['direction'], p['who'], p['what'], due, (base + dt.timedelta(days=p['due_days'] or 1)).isoformat(), ids[p['event']], account,
                    p['status'], stamp(2 * 24 * 60, base), stamp(60, base)))
    # Still needed? as a quiet week leaves it (still_needed.py): asked a week ago without an answer (folded), and asked today
    import assistant
    for days in (8, 0):
        assistant.Store.still_needed_ask(db, (base - dt.timedelta(days=days)).isoformat())


# What the company look-up would say of each made-up company: industry, size and country (the Organizations filter).
COMPANY_FACTS = {'Northwind Analytics': ('Computer Software', '51-200', 'us'), 'Brightpath Logistics': ('Logistics and Supply Chain', '201-500', 'nl'),
                 'Cobalt & Finch': ('Design', '2-10', 'gb'), 'Harborline Health': ('Hospital and Health Care', '1001-5000', 'us'),
                 'Quarry Lane Studios': ('Media Production', '11-50', 'gb'), 'Tidewater Foods': ('Food Production', '501-1000', 'be'),
                 'Meridian Robotics': ('Machinery', '51-200', 'de'), 'Pinecrest Legal': ('Law Practice', '11-50', 'us'),
                 'Saltmarsh Media': ('Online Media', '11-50', 'gb'), 'Vantage Rail': ('Railroad Manufacture', '1001-5000', 'de'),
                 'Orchard Street Bakery': ('Food and Beverages', '2-10', 'be'), 'Kestrel Energy': ('Renewables and Environment', '201-500', 'nl'),
                 'Glasswing Apps': ('Computer Software', '2-10', 'be'), 'Fernhill Schools': ('Education Management', '51-200', 'gb'),
                 'Ironbark Outdoor': ('Sporting Goods', '11-50', 'ca')}


# What a few of them say they do best (a look-up's specialties: the organization's page and the Specialty filter).
COMPANY_SPECIALTIES = {'Northwind Analytics': ['Data Warehousing', 'Business Intelligence', 'Forecasting', 'Dashboards'],
                       'Meridian Robotics': ['Industrial Automation', 'Pick and Place', 'Machine Vision'],
                       'Kestrel Energy': ['Solar Parks', 'Battery Storage', 'Grid Services']}
# What the person look-up would say of one story contact: about text and role history (their page).
PERSON_LOOKUPS = {'mila@northwindanalytics.example': {
    'title': 'Head of Data', 'company': 'Northwind Analytics', 'company_domain': 'northwindanalytics.example',
    'about': 'Turning messy data into decisions. Leading the data team at Northwind; before that, analytics for retail and logistics.',
    'since': '2022-03', 'before': [{'title': 'Analytics Lead', 'company': 'Brightpath Logistics'}, {'title': 'Data Analyst', 'company': 'Tidewater Foods'}]}}


def load_companies(db, fixture, base):
    """Every made-up company by its own name ("Saltmarsh Media"), as the company look-up would give it on a real
    Machine; without one the Graph would spell it from its domain ("Saltmarshmedia")."""
    for c in fixture.get('companies') or ():
        industry, size, country = COMPANY_FACTS.get(c['name'], (None, None, None))
        profile = {'name': c['name'], **({'industry': industry, 'size': size, 'country': country} if industry else {})}
        if c['name'] in COMPANY_SPECIALTIES:
            profile['specialties'] = COMPANY_SPECIALTIES[c['name']]
        db.execute("INSERT OR IGNORE INTO org_profiles(domain,status,profile,fetched_at) VALUES(?,'found',?,?)",
                   (c['domain'], json.dumps(profile), base.isoformat()))
    import enrichment
    for address, profile in PERSON_LOOKUPS.items():
        enrichment.save_person(db, 'email:' + address, 'found', profile, base.isoformat())


def load_boards(db, fixture, ids, base):
    """Graph > Projects > Board: each project labeled with its messages and moved through its stages by them, as a review
    would (graph.set_stage), one dragged by hand; their organizations' names as an enrichment service would give them."""
    import graph
    for board in fixture.get('boards') or ():
        if board.get('suggestion'):  # projects on no board yet, and a review's suggestion of a board for them
            sug = board['suggestion']
            for p in sug['projects']:
                graph.label(db, [ids[k] for k in p['events'] if k in ids], p['name'], 'review', base.isoformat())
            graph.suggest_board(db, {**sug, 'projects': [p['name'] for p in sug['projects']]}, 'review', base.isoformat())
            continue
        graph.save_board(db, {'name': board['name'], 'stages': board['stages'], 'about': board.get('about', '')}, base.isoformat())  # the owner saved it
        for p in board['projects']:
            graph.label(db, [ids[k] for k in p['events'] if k in ids], p['name'], 'review', base.isoformat())
            for i, m in enumerate(p['moves']):
                graph.set_stage(db, p['name'], m['stage'], 'review', base.isoformat(), board=board['name'], stages=board['stages'], reason=m['reason'],
                                event_id=ids[m['event']], next_step=p['next'] if i == len(p['moves']) - 1 else None, org=p['org'])
            if p.get('by_hand'):
                node = 'project:' + str(db.execute('SELECT id FROM projects WHERE name=?', (p['name'],)).fetchone()[0])
                graph.set_stage(db, node, p['by_hand']['stage'], 'owner', stamp(p['by_hand']['days_ago'] * 24 * 60, base))
            if p.get('success'):  # done when, as a review suggested it, and the live page that proved one (no network here)
                import project_success
                pid = db.execute('SELECT id FROM projects WHERE name=?', (p['name'],)).fetchone()[0]
                project_success.set_condition(db, pid, p['success']['condition'], p['success']['proof'], 'review', base.isoformat())
                if p['success'].get('event'):
                    project_success.record_proof(db, pid, ids[p['success']['event']], p['success']['url'], base.isoformat())
            db.execute("INSERT OR IGNORE INTO org_profiles(domain,status,profile,fetched_at) VALUES(?,'found',?,?)",
                       (p['org'], json.dumps({'name': p['org_name'], 'industry': 'Software'}), base.isoformat()))
    # Follow-ups on for the partner board (follow_ups.py), asking first: the header and the cards show the next one
    import follow_ups
    follow_ups.ensure(db)
    row = db.execute("SELECT id FROM boards WHERE name='Partner listings'").fetchone()
    if row:
        follow_ups.save(db, 'board', row[0], {'on': True}, base.isoformat())
    import project_success  # what a review run sees in their way (follow-ups on here, so no to-do of its own)
    project_success.monitor(db, base.isoformat())
    # Each board has looked through the history already: its header says what that found
    db.execute("UPDATE board_backfills SET state='done',started_at=?,finished_at=?", ((base - dt.timedelta(hours=1)).isoformat(), base.isoformat()))


def load_reviews(db, ids, base, assistant, fixture=None):
    """Reviews ran through the day: every signal has been read."""
    items = [{'id': i, 'version': 1} for i in ids.values()]
    for n, chunk in enumerate(range(0, len(items), 60)):
        at = 60 * (n + 1)
        run_id = f'sandbox-run-{n}'
        db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at,finished_at,attempts,planned) VALUES(?,'ok',?,?,?,1,?)",
                   (run_id, stamp(at, base), stamp(at - 4, base), stamp(at - 4, base), len(items[chunk:chunk + 60])))
        db.execute("INSERT INTO analyses(id,started_at,finished_at,items,status,summary,owner_session,owner_run) VALUES(?,?,?,?,'complete',?,?,?)",
                   (f'sandbox-analysis-{n}', stamp(at, base), stamp(at - 4, base), json.dumps(items[chunk:chunk + 60]), 'Read and sorted.',
                    assistant.REVIEW_SESSION_PREFIX + run_id, run_id))
    last = fixture.get('last_check') if fixture else None
    if last:  # the last check of new email, with the review's reason for each thread it made no to-do for (check_now.mail_check)
        from machine.store import review_whys
        started, finished = last['minutes']
        items = [{'id': ids[k], 'version': 1} for k in last['events'] if k in ids]
        whys = {ids[k]: {'no_todo': last['why'][k]} for k in last['events'] if k in ids and k in last['why']}
        db.execute("INSERT INTO review_runs(run_id,status,started_at,updated_at,finished_at,attempts,planned) VALUES(?,'ok',?,?,?,1,?)",
                   ('sandbox-run-last', stamp(started, base), stamp(finished, base), stamp(finished, base), len(items)))
        db.execute("INSERT INTO analyses(id,started_at,finished_at,items,whys,status,summary,owner_session,owner_run) VALUES(?,?,?,?,?,'complete',?,?,?)",
                   ('sandbox-analysis-last', stamp(started, base), stamp(finished, base), json.dumps(items), review_whys.text(whys), 'Read and sorted.',
                    assistant.REVIEW_SESSION_PREFIX + 'sandbox-run-last', 'sandbox-run-last'))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--dir', default='/tmp/machine-sandbox')
    parser.add_argument('--state', default='busy')
    parser.add_argument('--port', type=int, default=8870)
    parser.add_argument('--machine', metavar='CONFIG', help="a demo Machine: its config.json (see above)")
    parser.add_argument('--app', default=str(ROOT), help='with --machine: the installed app (default: this checkout)')
    args = parser.parse_args()
    if args.machine:
        sys.path.insert(0, args.app)
        print(json.dumps(fill_machine(json.loads(Path(args.machine).expanduser().read_text()))))
        return
    config, path = load(args.dir, parse_states(args.state), args.port, args.port + 1)
    print(path)


if __name__ == '__main__':
    main()
