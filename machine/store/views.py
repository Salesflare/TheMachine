"""The Store's views (refactor PR 18): what the dashboard shows of the Store. The snapshot, a to-do's card view with
its sources and what it's based on, a run's result and documents, task pages and the done page. A mixin of Store
(assistant.py), like App's mixins. Moved out of assistant.py as is."""
import datetime as dt
import copy
import hashlib
import json
import re
import sqlite3
import time
import urllib.request

import agent_jobs
import bounces
import browser_login
import calendar_clashes
import chat_files
import clear_pace
import doc_writes
import follow_ups
import gap_note
import graph
import lookalike
import learning_loop
import locale_prefs
from machine.browser import (
    browser_link,
    browser_view_link,
    browser_wait,
    safe_link,
    same_site,
    signin_link,
    TAB_LOOK,
    task_page,
)
from machine.cards import (
    blocker_questions,
    card_draft,
    card_recipients,
    group_sender,
    looks_done,
    looks_done_at,
    SOURCE_DM,
    source_line_shown,
    SOURCE_RAW,
)
from machine.chat import chat_result_files
from machine.config import WORKSPACE
from machine.faults import FAULT_WHERE
from machine.sources.connectors import crm_sync_health, docs_health, read_window, silent_failure, UNNAMED, whatsapp_history
from machine.sources import groups
from machine.sources.android import android_app_shown
from machine.sources.gmail import phone_link
from machine.sources.salesflare import salesflare_progress
from machine.sources.slack import slack_first_import_progress, SLACK_ID, slack_name_table, slack_named
from machine.store import history as history_store
from machine.store import graph_identifiers
from machine import names, stamps
from machine.store.cards import source_kind, source_lead, use_view
from machine.store.conversation import ConversationStore
from machine.store.decisions import checking_in, handoff_wait, handoffs_of, owner_area_open, send_retry_ok, skill_update_view, UNDO_MERGE
from machine.store.events import SET_ASIDE_AFTER
from machine.store.facts import suggestion_scope
from machine.store import message_view
from machine.store import review_last_look
from machine.store.review import own_message, REVIEW_SESSION_PREFIX
from machine.text import _address
import meeting_prep
import bring_in
import missed_work
import next_actions
import own_addresses
import recurring
import routine_changes
import routine_offers
import shared_connectors
import skills
from sources import CALENDAR_SERVICES, MAIL_SERVICES
import still_needed
from timeutil import local_tz, now
import todo_areas
import todo_org
import whatsapp_images
from machine import todo_kinds, todo_states
from machine.owner_error import OwnerError
import timeutil

# What card_views adds to the to-dos, kept between status polls (each 30 s) while none of the tables it reads changed (on
# a quiet Machine, between polls only Connections' sync tables do), the to-dos' own rows are the same and within
# CARD_KEEP_S (what it works out from the clock: "3 days ago", Still needed?). CARD_TABLES: all it reads (a test checks
# that). Kept as deep copies: the status changes what it is handed, never the kept copy.
CARD_TABLES = ('action_jobs', 'agent_jobs', 'calendar_clashes', 'chat_files', 'decision_annotations', 'decision_asks', 'decisions', 'digest_items', 'email_bounces',
               'events', 'facebook_birthdays', 'facts', 'feedback_prompts', 'fleet_meta', 'fleet_out', 'graph_events', 'graph_identifiers', 'graph_nodes',
               'identity_names', 'mail_cleanup_items', 'person_facts', 'preparation_calls', 'preparation_runs', 'preparations', 'projects',
               'promises', 'recap_items', 'recurring_series', 'routine_changes', 'routines', 'skill_clusters', 'skill_task_decided', 'skills',
               'slack_members', 'subs_items', 'suggestions', 'task_pages', 'thread_snoozes', 'whatsapp_photos')
CARD_KEEP_S = 120
CARDS = stamps.Kept(4)
# The status is kept between polls by the change counters of every table but these (StatusApp.status_kept): tables it
# never reads that are written all day in the background (meaning search, logs, the Network's transport, runs). A
# test checks a status build reads none of them; a table not listed is counted, so a new one never leaves it stale.
STATUS_QUIET = ('activity_accounts', 'activity_blocks', 'agent_result_receipts', 'ai_activity', 'ai_folded', 'ai_tokens', 'ai_writes',
                'android_inbox', 'android_receipts', 'chat_fast_sessions', 'digest_spend', 'draft_seen', 'email_bounce_cc_scan',
                'email_bounce_scan', 'event_passages', 'event_vector_skips', 'event_vectors', 'fact_vectors', 'fleet_learn_vectors',
                'gateway_starts', 'meet_log', 'network_aliases', 'network_looked', 'network_outbox', 'network_pins', 'network_replies',
                'network_sealed', 'network_taken', 'network_twins', 'person_summary_runs', 'plain_key_pass', 'record_changes',
                'retention_runs', 'routine_runs', 'store_fixes', 'sync_daily', 'talk_lines', 'team_blobs', 'team_files', 'team_mail')
# What only the connections' cards read (connector_views): a sync round writes these, and only the cards are made again.
SYNC_TABLES = ('android_feed_health', 'checkpoints', 'history_backfill', 'sync_activity')
# Tables the status reads only a part of, kept by that part's own counter (stamps): activity_seen's opens of a to-do
# (stamps.activity_opened). Its other rows come from the page's own load and poll, which made each next status build again.
STATUS_NARROW = {'activity_seen': 'activity_opened'}


def status_tables(db):
    """The tables the status is kept by: all but STATUS_QUIET, SQLite's own, data_stamps (the counters themselves) and
    virtual tables with their shadow tables (full-text search, which the status never reads). A table in STATUS_NARROW
    is there by the name of its part's counter."""
    rows = db.execute("SELECT name,sql FROM sqlite_master WHERE type='table'").fetchall()
    virtual = tuple(r[0] + '_' for r in rows if str(r[1] or '').upper().startswith('CREATE VIRTUAL'))
    return sorted(STATUS_NARROW.get(r[0], r[0]) for r in rows if r[0] not in STATUS_QUIET and r[0] != 'data_stamps'
                  and not r[0].startswith('sqlite_') and not str(r[1] or '').upper().startswith('CREATE VIRTUAL')
                  and not r[0].startswith(virtual))
DONE_FIRST = 30  # the done to-dos the dashboard's status gets: its Done list's first page (dashboard donePager)


def shown_job(job):
    """A preparation row as the to-do shows it (agent_jobs.shown_preparation): once a handed-off job took over from a
    stuck run, that run's error and reason are not the to-do's any more (the row keeps them)."""
    shown = job.pop('shown', None) or job['status']
    if shown != job['status']:
        job.update(status=shown, error=None, reason=None)
    return job



def source_group(service):
    """A connected source's group, worked out as + Add's catalog does (onboarding.catalog): the dashboard picks its tab by it."""
    import onboarding  # here: onboarding loads the connectors, which the store's other users don't need
    return groups.group_of(service, onboarding.setup_of(service).get('group'))


def covered_name(accounts, account):
    """The name of the owner's own connection that reads what this Fleet share reads, so the share rests; else None."""
    own = shared_connectors.covered_by(accounts, account)
    found = next((a for a in accounts if a.get('id') == own), None) if own else None
    return names.account_name(found, accounts) if found else None


def skill_labels(cluster):
    return {'accept': 'Update ' + cluster['target_name'] if cluster['target_id'] else 'Create skill', 'reject': 'Not now'}


# A routine draft's step (routines_app.DRAFT_ACTS), named on its to-do's lead button instead of Do it
ROUTINE_ACT = {'post': 'Post it', 'send': 'Send it'}
ROUTINE_ID = re.compile(r'[a-f0-9]{32}')


def routine_view(db, metas):
    """The routine a to-do came from, when its evidence is a routine's draft (routines_app.routine_draft_todo): {'id',
    'name', 'live', 'act'}. live: the routine is still on the Routines page (on or paused), so its source line links to
    it there; its name is its name now (a rename shows), else the one it had. act: post or send, or None. None for any
    other to-do. metas: the to-do's evidence metadata, as stored."""
    for meta in metas:
        try:
            m = meta if isinstance(meta, dict) else json.loads(meta or '{}')
        except (ValueError, TypeError):
            continue
        rid = m.get('routine') if isinstance(m, dict) else None
        if not isinstance(rid, str) or not ROUTINE_ID.fullmatch(rid):
            continue
        try:
            row = db.execute('SELECT name,state FROM routines WHERE id=?', (rid,)).fetchone()
        except sqlite3.Error:
            row = None
        live = bool(row) and row['state'] in ('on', 'paused')
        name = ' '.join(str((row['name'] if live else None) or m.get('sender_display') or '').split())
        return {'id': rid, 'name': name, 'live': live, 'act': m.get('act') if m.get('act') in ROUTINE_ACT else None}
    return None


def area_hint(db, suggestion, accounts, here):
    """The area a to-do's people point to (todo_areas.pointed), from the Graph: their side, the accounts they were heard
    on and their organization's domain. None when there are not several areas to pick from or nothing points anywhere."""
    if sum(a['id'] != here for a in todo_areas.areas(accounts)) < 2:
        return None  # one other area: More moves straight to it, no picker
    try:
        ids = [int(i) for i in json.loads(suggestion.get('event_ids') or '[]')]
        if not ids:
            return None
        marks = ','.join('?' for _ in ids)
        rows = db.execute(f"SELECT DISTINCT n.info,o.info org_info FROM graph_events g JOIN graph_nodes n ON n.id=g.node_id LEFT JOIN graph_nodes o "
                          f"ON o.id=json_extract(n.info,'$.org') WHERE g.direct=1 AND n.kind='person' AND g.event_id IN ({marks})", ids).fetchall()
        people = []
        for r in rows:
            info, org = json.loads(r['info'] or '{}'), json.loads(r['org_info'] or '{}')
            people.append({'side': info.get('side'), 'accounts': info.get('accounts') or [], 'org_domain': org.get('domain')})
    except (sqlite3.Error, ValueError, TypeError):
        return None
    free = lambda value: (lambda d: '' if d in graph.FREEMAIL else d)(own_addresses.email_domain(value))
    return todo_areas.pointed(people, accounts, here, free)


# Chats read as one thread on the dashboard (events-email.js chatThreadHTML): the conversation named once, then turns.
CHAT_KINDS = {'slack.message', 'teams.message', 'whatsapp.message', 'telegram.message', 'signal.message', 'linkedin.message', 'x.dm', 'fleet.message',
              'intercom.conversation', 'fleet.intercom'}


INTERCOM_PART = message_view.INTERCOM_PART


def chat_view(kind, m, body, occurred_at):
    """For a chat message: the conversation's name ("#support", a Slack DM's other person with dm, a WhatsApp chat) and,
    for an Intercom conversation, its messages as turns (message_view.intercom_turns: who wrote each, customer, team
    or bot, and only the parts that say something). Nothing for other kinds."""
    if kind not in CHAT_KINDS:
        return {}
    out = {'chat': ''}
    if kind == 'slack.message':
        name = str(m.get('channel_name') or '')
        dm = m.get('conversation_type') == 'dm' or name.startswith('DM ')
        out.update(chat=name[3:].strip() if dm and name.startswith('DM ') else ('#' + name if name else ''), dm=dm)
    elif kind in ('intercom.conversation', 'fleet.intercom'):
        out['chat'] = m.get('contact_name') or m.get('from_name') or m.get('contact_email') or m.get('from') or ''
        turns = message_view.intercom_turns(m, body, occurred_at)
        if turns:
            out['turns'] = turns
    else:
        out['chat'] = str(m.get('chat_name') or '')
    out['chat'] = out['chat'][:200]
    return out


def sender_first_name(metadata):
    """The first name of who sent a message, as the message names them ("Sam Lee <sam@…>" is Sam), or '' when it
    carries only an address, a number or a chat handle."""
    m = metadata or {}
    raw = str(m.get('sender_display') or m.get('from') or m.get('chat_name') or '')
    who = re.sub(r'\s*<[^>]*>?', '', raw).strip().strip('"').strip()
    who = re.sub(r'\s+via\s.*$', '', str(group_sender(who))).strip().strip("'").strip()  # "'Sam Lee' via Sales": Sam
    if not who or '@' in who or SLACK_ID.search(who) or SOURCE_RAW.search(who):
        return ''
    # A mail tool that shows the mailbox as the name ("frontdesk <frontdesk@…>", "billing <billing@…>"): not a name
    local = (_address(raw) or _address(m.get('from'))).split('@')[0]
    if local and not who[:1].isupper() and re.sub(r'[._+-]', '', who.casefold()) == re.sub(r'[._+-]', '', local.split('+')[0]):
        return ''
    if ',' in who:  # "Lee, Sam"
        who = who.split(',', 1)[1].strip() or who
    first = (who.split() or [''])[0]
    return first if re.fullmatch(r"[^\W\d_][\w'’-]*", first) else ''


def slack_people_names(db, ids):
    """{Slack member id: name} as the people graph shows them (the name from their mail over a lower-case Slack
    handle, or the owner's own), else as users.info gave it. Kept until a name, a person or a member changes: the to-do
    list names the same few members on every status poll, and each time was a pass over every person."""
    ids = tuple(sorted({i for i in ids if isinstance(i, str) and re.fullmatch(r'[UW][A-Z0-9]{8,11}', i)}))
    return dict(SLACK_PEOPLE.get(ids, stamps.stamp(db, ('identity_names', 'graph_nodes', 'slack_members')), lambda: _slack_people_names(db, ids)))


SLACK_PEOPLE = stamps.Kept(16)  # slack_people_names, by stamp


def _slack_people_names(db, ids):
    names = slack_name_table(db, ids)
    if not ids:
        return names
    try:
        rows = graph_identifiers.rows(db, 'n.name,n.info', ['slack:' + i for i in ids],
                                      "SELECT name,info FROM graph_nodes WHERE kind='person' AND (" + ' OR '.join(['info LIKE ?'] * len(ids)) + ')',
                                      ['%"slack:' + i + '"%' for i in ids])
    except sqlite3.OperationalError:
        return names  # no graph yet
    for name, info in rows:
        try:
            found = set(json.loads(info or '{}').get('identifiers') or ())
        except ValueError:
            continue
        names.update({i: name for i in ids if 'slack:' + i in found and name and name not in graph.SOURCE_NAMES})  # not "Slack", a node no name was known for
    return names


def address_names(db, addresses):
    """message_view.address_names: never a source's own name ("Slack", "Stripe") as a person's name."""
    return message_view.address_names(db, addresses)


# The who of a stored source line ("email from ann@client.com · Sun 8 Nov")
SOURCE_WHO = re.compile(r'^(?:Source: )?.+? (?:from|to) (.+?)(?: · [^·]+?)?(?: \(\+\d+ more\))?$')


def source_lines_shown(db, cards):
    """The cards' source lines as source_line_shown writes them, Slack members by their names (slack_people_names),
    and a sender stored by address by the name the graph knows for it (address_names). One saved before kinds nothing
    names lost their line (cards.shown_source) says "signal": none."""
    for c in cards:
        if re.match(r'Source: signal\b', str(c.get('source_line') or '')):
            c['source_line'] = None
    lines = [c.get('source_line') for c in cards if c.get('source_line')]
    names = slack_people_names(db, {m[1] for line in lines for m in SLACK_ID.finditer(str(line))})
    people = address_names(db, {a for line in lines if (m := SOURCE_WHO.match(str(line))) for a in message_view.bare_addresses(m[1])})
    for c in cards:
        if c.get('source_line'):
            line = source_line_shown(c['source_line'], names)
            m = people and SOURCE_WHO.match(str(line))
            name = m and people.get(m[1].strip().strip('<>').lower())
            c['source_line'] = line[:m.start(1)] + name + line[m.end(1):] if name else line


def source_marks(db, cards):
    """Each source line's icon from the event the line names (cards.source_lead): its kind, account and, for a phone
    notification, its app (todos-logos.js sourceMark), so "WhatsApp to Sam (+2 more)" never wears the mark of an
    email among the other messages. None when no event fits; the dashboard then reads the line's words."""
    held = {c['id']: [i for i in json.loads(c.get('event_ids') or '[]') if isinstance(i, int)] for c in cards if c.get('source_line')}
    ids = sorted({i for v in held.values() for i in v})
    rows = {r['id']: dict(r) for r in db.execute('SELECT id,account_id,kind,occurred_at,title,metadata FROM events WHERE id IN '
                                                   '(SELECT value FROM json_each(?))', (json.dumps(ids),))} if ids else {}
    for card in cards:
        if card['id'] not in held:
            continue
        try:  # only a meeting's notes need the meeting looked up (meeting_mail.lead); any other line names its lead's kind
            meeting = str(card['source_line']).startswith('Source: notes from ')
            lead = source_lead([rows[i] for i in held[card['id']] if i in rows], card['source_line'], db if meeting else None)
        except (sqlite3.Error, ValueError, TypeError):
            lead = None
        if lead:
            m = json.loads(lead['metadata'] or '{}')
            card['source_mark'] = {'kind': lead['kind'], 'account_id': lead['account_id'],
                                   'app': (m.get('package_name') if isinstance(m, dict) else None) or None}


def based_on_views(db, cards):
    """Each to-do's based_on (Store.mark_based_on) as the to-do shows it: who wrote it by name (a Slack member by
    their name, never their id), the Slack channel it is in, when, and a link to it. One gone since is left out."""
    ids = {c['based_on'] for c in cards if isinstance(c.get('based_on'), int)}
    rows = {r['id']: r for r in slack_named(db, [dict(r) for r in db.execute(
        'SELECT id,account_id,kind,occurred_at,title,metadata FROM events WHERE deleted=0 AND id IN (' + ','.join('?' * len(ids)) + ')', sorted(ids))])} if ids else {}
    leads = source_leads(db, [c for c in cards if c.get('based_on') in rows])
    for card in cards:
        row = rows.get(card.get('based_on'))
        if not row or leads.get(card['id']) == row['id']:  # the source line already names it: one line per message, never two
            card['based_on'] = None
            continue
        m = row['metadata'] if isinstance(row['metadata'], dict) else json.loads(row['metadata'] or '{}')
        channel = str(m.get('channel_name') or '') if row['kind'] == 'slack.message' else ''
        url = m.get('source_url')
        card['based_on'] = {'event_id': row['id'], 'who': sender_first_name(m) or None, 'kind': source_kind(row['kind']),
                            'where': '#' + channel.lstrip('#') if channel and not SOURCE_DM.fullmatch(channel) and not SLACK_ID.search(channel) else None,
                            'at': row['occurred_at'], 'url': url if isinstance(url, str) and urllib.parse.urlsplit(url).scheme == 'https' else None}


def source_leads(db, cards):
    """{card id: the event its source line names} (source_line: the first of its evidence that isn't the owner's own
    to-do or an update's note), so a based_on that is that same message isn't shown a second time."""
    held = {c['id']: [i for i in json.loads(c.get('event_ids') or '[]') if isinstance(i, int)] for c in cards}
    ids = sorted({i for v in held.values() for i in v})
    kinds = {r['id']: r['kind'] for r in db.execute('SELECT id,kind FROM events WHERE id IN (' + ','.join('?' * len(ids)) + ')', ids)} if ids else {}
    return {cid: next((i for i in v if i in kinds and kinds[i] not in ('owner.card', 'machine.parked_fix')), None) for cid, v in held.items()}


def stopped_step(db, suggestion, pre=None):
    """One true line for a card whose confirmed step stopped without going through (paused: its run was blocked, timed
    out, or a snooze or close canceled it). It replaces the card's earlier result text, which still reads as if the step
    were ready or done: what didn't happen, why in a few words, and when it carries on. None otherwise.
    A final step that new work replaced before its result was saved (finish_uncertain, see queue_preparation) counts too
    while that work has no result yet: the card still shows the step's preview. One that was paused then is not done;
    one without that record may have gone through, so it is not confirmed. pre: card_reads for a list of cards."""
    prep = pre['preparations'].get(suggestion['id']) if pre else \
        db.execute('SELECT status,reason,error FROM preparations WHERE suggestion_id=?', (suggestion['id'],)).fetchone()
    step, prefix = None, ''
    for row in (db.execute("SELECT status,payload FROM action_jobs WHERE suggestion_id=? AND status IN ('paused','finish_uncertain') ORDER BY updated_at DESC", (suggestion['id'],))
                if not pre or suggestion['id'] in pre['jobs'] else ()):
        payload = json.loads(row['payload'])
        if row['status'] == 'paused':
            step, prefix = payload, 'Not done yet: ' if payload.get('kind') == 'finish' else 'Not prepared yet: '
            break
        result = payload.get('finish_result') or {}
        # Its own uncertain result is the card's text then, or newer work saved a result: the card says what is true.
        if result.get('body') == suggestion.get('body') or not prep or prep['status'] == 'done':
            break
        step, prefix = payload, 'Not done yet: ' if result.get('was') == 'paused' else 'Not confirmed yet: '
        break
    if not step:
        return None
    label = ' '.join(str(step.get('label') or '').split())[:80] or 'The next step'
    why = ''
    if prep and prep['error'] in ('completion_unconfirmed', 'ai_run_timed_out'):
        why = 'it ran too long'
    elif prep and prep['error']:
        why = 'the run failed'
    elif prep and prep['reason']:
        why = re.split(r'[.;:!?]|,? so |,? but | because ', str(prep['reason']).strip(), maxsplit=1)[0].strip()
        why = why[:1].lower() + why[1:] if why[1:2] and why[1:2].islower() else why
        why = why if len(why) <= 70 else ''
    line = prefix + label + (f' ({why}).' if why else '.')
    if suggestion.get('status') == 'snoozed' and suggestion.get('snoozed_until'):
        back = dt.datetime.fromisoformat(suggestion['snoozed_until']).astimezone(local_tz())
        today = timeutil.clock(local_tz()).date()
        at = locale_prefs.clock_text(back) if back.date() == today else locale_prefs.clock_text(back) + ' tomorrow' if (back.date() - today).days == 1 else locale_prefs.at_text(back)
        line += f' It carries on when the to-do comes back, {at}.'
    elif prep and prep['status'] == 'blocked':
        line += ' Try again carries it on.'
    return line


def chat_linked_files(db, suggestion_id):
    """The result files each of this card's saved results linked (what its chat shows as chips)."""
    files = []
    for r in db.execute("SELECT c.params FROM preparation_calls c JOIN preparation_runs p ON p.job_id=c.job_id "
                        "WHERE p.suggestion_id=? AND c.tool='assistant_signals' AND (c.error IS NULL OR c.error='')", (suggestion_id,)):
        try:
            params = json.loads(r['params'])
        except (ValueError, TypeError):
            continue
        args = params.get('args') if isinstance(params, dict) and isinstance(params.get('args'), dict) else {}
        if params.get('action') == 'prepare' and args.get('suggestion_id') == suggestion_id:
            files += chat_result_files(args.get('body'))[1]
    return files


def review_run_view(db, run):
    """A review run with how far it got: what it claimed, saved (done_count of planned) and from which accounts."""
    claims = db.execute('SELECT status,items FROM analyses WHERE owner_run=? AND owner_session=?',
                        (run['run_id'],REVIEW_SESSION_PREFIX+run['run_id'])).fetchall()
    run['review_saved'] = bool(claims) and all(c['status']=='complete' for c in claims)
    run['checked_count'] = sum(sum(not i.get('excluded') and not i.get('deferred') for i in json.loads(c['items']))
                               for c in claims if c['status']=='complete')
    run['done_count'] = sum(len(json.loads(c['items'])) for c in claims if c['status']=='complete')
    items = [i for c in claims for i in json.loads(c['items'])]
    ids = list({i['id'] for i in items})
    versions, accounts = {}, set()
    for n in range(0, len(ids), 500):
        chunk = ids[n:n+500]
        for r in db.execute(f"SELECT id,analyzed_version,account_id FROM events WHERE id IN ({','.join('?'*len(chunk))})", chunk):
            versions[r['id']] = r['analyzed_version']
            accounts.add(r['account_id'])
    run['account_ids'] = sorted(accounts)
    run['pending_count'] = sum(i['id'] in versions and versions[i['id']] < i['version'] for i in items)
    run['claimed_count'] = sum(len(json.loads(c['items'])) for c in claims)
    run['duration_seconds'] = max(0,int((dt.datetime.fromisoformat(run['finished_at'] or now())-
                                         dt.datetime.fromisoformat(run['started_at'])).total_seconds()))
    return run


def card_reads(db, cards):
    """What suggestion_result reads for each card, read once for all of them (the status payload read it per card,
    some 750 reads for 127 cards): their messages' links, their preparations, and which cards have a skill proposal,
    a proposed or decided skill, or action jobs at all (only those are looked up one by one, as before)."""
    ids = json.dumps([c['id'] for c in cards])
    events = set()
    for card in cards:
        try:
            events.update(json.loads(card['event_ids'] or '[]'))
        except (ValueError, TypeError):
            pass
    pre = {'events': {r['id']: r['metadata'] for r in db.execute('SELECT id,metadata FROM events WHERE id IN (SELECT value FROM json_each(?))', (json.dumps(sorted(events, key=str)),))},
           'clusters': {r[0] for r in db.execute('SELECT DISTINCT suggestion_id FROM skill_clusters WHERE suggestion_id IN (SELECT value FROM json_each(?))', (ids,))},
           'jobs': {r[0] for r in db.execute('SELECT DISTINCT suggestion_id FROM action_jobs WHERE suggestion_id IN (SELECT value FROM json_each(?))', (ids,))},
           'preparations': {r['suggestion_id']: r for r in db.execute('SELECT suggestion_id,job_id,status,reason,error FROM preparations WHERE suggestion_id IN (SELECT value FROM json_each(?))', (ids,))}}
    try:  # skills.for_task reads these two; before their columns exist it looks per card as before
        pre['skills'] = {r[0] for r in db.execute("SELECT task FROM skills WHERE task IN (SELECT value FROM json_each(?)) AND status='proposed' AND origin='proposed' "
                                                  "UNION SELECT task FROM skill_task_decided WHERE task IN (SELECT value FROM json_each(?))", (ids, ids))}
    except sqlite3.OperationalError:
        pass
    # A kind's items (todo_kinds.reads: a mail cleanup's, a digest's), and the newest handoff of each (handoff_wait):
    # before their tables exist (a Machine without them yet, or without a Fleet) each card looks as before
    pre.update(todo_kinds.reads(db, ids))
    try:
        pre['handoffs'] = handoffs_of(db, [c['id'] for c in cards])
    except sqlite3.OperationalError:
        pass
    return pre


class ViewsStore(ConversationStore):
    """Store methods for what the dashboard shows, with a source message's conversation (ConversationStore)."""

    def event_views(self, ids):
        """Collected messages, in the given order, for reading on the dashboard."""
        ids = [int(i) for i in ids]
        with self.connect() as db:
            rows = slack_named(db, [dict(r) for r in db.execute('SELECT id,account_id,source_id,kind,occurred_at,title,body,metadata FROM events WHERE id IN (' + ','.join('?' for _ in ids) + ')', ids)]) if ids else []
            own = own_addresses.yours(db, self.config) if rows else set()
            photos = {r['id']: whatsapp_images.shown(db, {'database': str(self.path)}, json.loads(r['metadata']))
                      for r in rows if r['kind'] == 'whatsapp.message'}  # a WhatsApp photo the Machine kept (whatsapp_images.py)
        own |= {str(a.get('email') or '').lower() for a in self.accounts if a.get('service', 'gmail') in MAIL_SERVICES and '@' in str(a.get('email') or '')}
        rows.sort(key=lambda r: ids.index(r['id']))
        result = []
        for r in rows:
            m = json.loads(r['metadata'])
            url = m.get('source_url')
            mine = m.get('from_me') or (r['kind'] == 'gmail.message' and _address(m.get('from')) in own)  # also from another address of theirs
            if r['kind'] == 'android.notification':
                m['app_name'] = android_app_shown(m.get('package_name'), m.get('app_name'))  # its app by name, never the package
            # A chat message is said by a person, never by its channel or chat (an unnamed Slack sender stays blank)
            chat = r['kind'] in CHAT_KINDS
            # an email's From as it is (the viewer mutes the address); any other message's sender by name, never a relay address
            sent_by = m.get('from') if message_view.view_of(r['kind']) == 'email' else message_view.sender_name(r['kind'], m)
            who = 'You' if mine else (m.get('sender_display') or sent_by or ('' if chat else m.get('chat_name') or m.get('app_name')
                   or (('#' + m['channel_name']) if m.get('channel_name') else '')) or '')
            body, details = r['body'], None
            if r['kind'] == 'machine.fault' and '\n' + FAULT_WHERE in body:  # code locations go under Details
                body, details = body.split('\n' + FAULT_WHERE, 1)
                body, details = body.strip(), FAULT_WHERE + details.rstrip()
            if r['kind'] == 'machine.fault':
                who = 'The Machine'
            photo = photos.get(r['id'])
            if photo:  # the photo shows; what it said stays with the message for the Machine (alt text: what it shows)
                said = body.split('\n\n' + whatsapp_images.MARK, 1)
                body = re.sub(r'^Sent image(?:\n|$)', '', said[0])  # the photo itself says that
                shows = re.search(r'(?m)^Shows: (.+)$', said[1]) if len(said) > 1 else None
                photo['alt'] = shows[1][:300] if shows else ''
            media = {} if photo else message_view.media_shown(r['kind'], m, body)  # a photo not kept, a video: its chip
            result.append(message_view.shape(r['kind'], {'kind': source_kind(r['kind']), 'from': str(who)[:300], 'to': str(m.get('to') or '')[:500],
                           'cc': str(m.get('cc') or '')[:500], 'title': r['title'][:500], 'occurred_at': r['occurred_at'],
                           **{key: str(m[head])[:500] for key, head in (('reply_to', 'reply-to'), ('bcc', 'bcc'), ('sender', 'sender'))
                              if m.get(head) and message_view.view_of(r['kind']) == 'email'},
                           'body': body[:20000], 'clipped': len(body) > 20000 or bool(m.get('truncated')),
                           **({'details': details[:4000]} if details else {}),
                           'url': url if isinstance(url, str) and urllib.parse.urlsplit(url).scheme == 'https' else None,
                           **({'phone_url': phone} if r['kind'] == 'gmail.message' and (phone := phone_link(url, m.get('thread_id'))) else {}),
                           'event_id': r['id'], 'gmail': {'account_id': r['account_id'], 'message_id': r['source_id']} if r['kind'] == 'gmail.message' else None,
                           **({'photo': photo} if photo else {}), **media,
                           **chat_view(r['kind'], m, body, r['occurred_at'])}, m))
        mail = [o for o in result if o.get('view') == 'email']
        rest = [o for o in result if o.get('view') != 'email']
        # outside email a sender is only a name: a chat's, its turns' and a payment's by the graph's name for the address
        said = [o.get('from') for o in rest] + [o.get('chat') for o in rest] + [t.get('from') for o in rest for t in o.get('turns') or ()]
        bare = message_view.bare_addresses(*(o.get(k) for o in mail for k in ('from', 'to', 'cc', 'bcc', 'reply_to')), *said)
        if bare:  # people by the name the graph knows for them, the address only when none is known
            with self.connect() as db:
                names = address_names(db, bare)
            for o in mail:
                for key in ('from', 'to', 'cc', 'bcc', 'reply_to'):
                    o[key] = message_view.named(o.get(key), names)
            for o in rest:
                for key in ('from', 'chat'):
                    if o.get(key):
                        o[key] = message_view.name_only(o[key], names)
                for t in o.get('turns') or ():
                    t['from'] = message_view.name_only(t.get('from'), names)
        return result

    def suggestion_result(self, suggestion, db, pre=None):
        """Only owner-workspace reports explicitly linked by this task are served. pre: card_reads for a list of cards."""
        files=[]
        for match in re.findall(r'memory/assistant/[^\s<>"\)]+', suggestion['body']):
            relative=match.rstrip('.,;]')
            candidate=(WORKSPACE/relative).resolve()
            if candidate.is_relative_to((WORKSPACE/'memory/assistant').resolve()) and candidate.is_file() and candidate.suffix.lower() in ('.md','.txt','.pdf'):
                files.append({'name':candidate.name,'path':relative})
        ids=json.loads(suggestion['event_ids'])
        originals=[]
        rows=[{'id':i,'metadata':pre['events'][i]} for i in dict.fromkeys(ids) if i in pre['events']] if pre else \
            sorted(db.execute('SELECT id,metadata FROM events WHERE id IN ('+','.join('?' for _ in ids)+')',ids).fetchall() if ids else [],key=lambda r:ids.index(r['id']))
        for row in rows:
            url=json.loads(row['metadata']).get('source_url')
            if isinstance(url,str) and urllib.parse.urlsplit(url).scheme in ('https','http') and url not in originals:
                originals.append(url)
        extra={'result_files':files,'original_urls':originals[:5]}
        routine=routine_view(db,[row['metadata'] for row in rows])
        if routine:  # "From your routine X", X a link to it; its step names the lead button (Post it) while it waits on the owner
            act=routine.pop('act')
            extra['routine']=routine
            if act and suggestion.get('status')=='pending':extra['labels']={'accept':ROUTINE_ACT[act]}
        # its kind's part (todo_kinds.py): a cleanup's or Subscriptions' picks per item, the digest's pieces, Facebook's import
        extra.update(todo_kinds.views(db,suggestion['id'],[row['metadata'] for row in rows],pre))
        if meeting_prep.is_briefing(suggestion.get('dedupe_key')):extra['briefing']=True  # a meeting briefing: only for reading (meeting_prep.py)
        proposal = (not pre or suggestion['id'] in pre['clusters']) and db.execute("SELECT * FROM skill_clusters WHERE suggestion_id=?", (suggestion['id'],)).fetchone()
        if proposal:
            extra['skill_proposal'] = {'name': proposal['name'], 'body': proposal['body'],
                                      'notes': [r[0] for r in db.execute('SELECT text FROM facts WHERE id IN (' + ','.join('?' for _ in json.loads(proposal['fact_ids'])) + ') ORDER BY id', json.loads(proposal['fact_ids']))]}
            if proposal['target_id']:
                extra['skill_proposal']['update'] = skill_update_view(db, proposal)
            elif proposal['related_name']:
                extra['skill_proposal']['related'] = {'name': proposal['related_name'], 'relation': proposal['relation'] or ''}
            if proposal['status'] in ('pending', 'declined', 'failed'):
                extra['labels'] = skill_labels(proposal)
        # A skill this to-do's run proposed (skills-propose --job): the card shows it and offers Create skill or Update skill
        proposed = skills.for_task(db, suggestion['id']) if not pre or 'skills' not in pre or suggestion['id'] in pre['skills'] else None
        if proposed:
            extra['proposed_skill'] = proposed
        # A routine's to-do whose note holds for its next runs too: Also change the routine (routine_changes.py). Read only
        # for a routine's to-do, so other cards cost no query.
        if suggestion.get('status') not in todo_states.CLOSED and any(json.loads(r['metadata'] or '{}').get('routine') for r in rows):
            change=routine_changes.view(db,suggestion['id'])
            if change:extra['routine_change']=change
        action=suggestion.get('next_action');action=json.loads(action) if isinstance(action,str) else action
        if action:
            states={r['revision']:{**{k:r[k] for k in ('status','error','message_id','snooze_status','snooze_until','snooze_error') if r[k] is not None or k in ('status','error','message_id')},
                                   # A follow-up stopped before it went (Stop sending, or by hand): a draft to review again, not a failed send
                                   **({'status':'cancelled','error':None} if r['status'] in ('blocked','cancelled') and r['error']==follow_ups.STOPPED else {}),
                                   **({'auto':True} if r['approval_id'].startswith('auto-merge:') else {}),
                                   **({'sent_at':r['updated_at']} if r['status']=='sent' else {}),
                                   # Held for a new message in the thread: which one, so the to-do shows it and offers a redo
                                   **({'held_by':held} if r['status']=='blocked' and r['error']==follow_ups.HELD and (held:=follow_ups.held_message(db,r['id'])) else {}),
                                   **({'url':doc_writes.link_of(r['message_id'])} if r['status']=='sent' and doc_writes.link_of(r['message_id']) else {}),  # a doc made: its link
                                   # Checked long enough without a trace: the owner may try again, and the card says so.
                                   **({'retry_ok':True,'error':'Last attempt unconfirmed: I found no sign of it going out. Check the conversation; if it isn’t there, try again.'}
                                      if send_retry_ok(r,json.loads(r['payload']).get('kind')) else {}),
                                   # A merged fix can be undone for a day.
                                   **({'undo_until':(dt.datetime.fromisoformat(r['updated_at'])+UNDO_MERGE).isoformat()} if r['status']=='sent' and str(r['message_id']).startswith('merge:') else {})}
                    for r in (db.execute('SELECT j.id,j.revision,j.status,j.error,j.message_id,j.approval_id,j.updated_at,j.payload,t.status snooze_status,t.until snooze_until,t.error snooze_error FROM action_jobs j LEFT JOIN thread_snoozes t ON t.job_id=j.id WHERE j.suggestion_id=?',(suggestion['id'],))
                              if not pre or suggestion['id'] in pre['jobs'] else ())}
            extra['next_actions']=[{**bounces.mark_draft(db,item),**({'state':states[item['revision']]} if item['revision'] in states else {})} for item in next_actions.visible_actions(action)]
            if action['kind']!='menu' and action['revision'] in states:extra['action_status']=states[action['revision']]
            # The draft Telegram shows in full on the card, so its Send there confirms directly (card_draft).
            shown=card_draft({**suggestion,**extra})
            if shown and shown['full']:extra['card_send']=shown['action']['revision']
        if suggestion.get('status') not in todo_states.CLOSED:
            stopped=stopped_step(db,suggestion,pre)
            if stopped:extra['step_stopped']=stopped
        prompt=suggestion.get('feedback_request_id') and db.execute('SELECT status,error FROM feedback_prompts WHERE request_id=?',(suggestion['feedback_request_id'],)).fetchone()
        if prompt:extra['change_prompt']=dict(prompt)
        job=pre['preparations'].get(suggestion['id']) if pre else db.execute('SELECT job_id,status,reason FROM preparations WHERE suggestion_id=?',(suggestion['id'],)).fetchone()
        waiting=browser_wait(db,job['job_id'],job['status'],reason=job['reason']) if job else None
        if waiting:
            extra['preparation_browser']={**waiting,'link':browser_link(self.config)}
            if waiting.get('sign_in'):extra['preparation_browser']['signin_url']=signin_link(self.config,suggestion['id'])
        if suggestion.get('status') in todo_states.TAKEN_ON:self.browser_view(db,suggestion,extra)
        if self.accounts and suggestion.get('account_ids') is not None:
            # the To-dos filter: one only about the Machine itself is neither Work nor Personal, under All only (todo_areas.machine_own).
            # Nor is one the owner added without an area that nothing placed yet (owner_area_open: the review places it by
            # what it is about, minutes later): the area it starts in is a stand-in, not a word on it
            unplaced=suggestion.get('origin')=='owner' and not suggestion.get('area') and bool(owner_area_open(db,suggestion['id']))
            extra['scope']=None if unplaced or todo_areas.machine_own(suggestion['account_ids'], self.accounts, suggestion.get('area')) else suggestion_scope(suggestion['account_ids'], self.accounts, suggestion.get('area'))
            extra['area']=todo_areas.current(suggestion['account_ids'], self.accounts, suggestion.get('area'))  # More, Move to: the other areas
            if extra['area'] and suggestion.get('status') in gap_note.OPEN_STATUSES:
                hint=area_hint(db,suggestion,self.accounts,extra['area'])  # Change area starts on where its people point
                if hint:extra['area_hint']=hint
        handoffs={'handoffs':pre['handoffs']} if pre and 'handoffs' in pre else {}
        wait=handoff_wait(db,suggestion,**handoffs)
        if wait:extra['handoff_wait']=wait
        still=handoff_wait(db,suggestion,awake=True,**handoffs)
        if still:extra['handoff_still']=still  # back on the list, still with them: the card says so, not "Needs you"
        if still and checking_in(db,suggestion):extra['handoff_checkin']=True  # Check in now: its nudge is drafted like any Do it
        return extra

    def browser_view(self, db, suggestion, extra):
        """A ready card whose own run worked in the Machine's browser links to that page there, not in the owner's own
        browser (where the run's sign-in and filled-in form are missing): its link-out to that site becomes View in
        browser's (browser:true, the dashboard's #browser-for address), and with none, a run that changed a page there
        (typed, clicked) gets one. Other links lose token-like query values. Read from the run's own browser steps.

        Only while that page is still open there (browser_open, also for the card's chat on an open card): a run that
        closed its tab, or a tab that is gone since, gets no View in browser, and its links stay plain links. Reopening
        the address would show a fresh page, not what the run left."""
        actions=extra.get('next_actions') or []
        for item in actions:
            if item.get('kind')=='open':item['url']=safe_link(item.get('url')) or ''
        page=self.task_pages(db,suggestion['id'])
        if not page or not self.page_open(page):return
        extra['browser_open']=True
        if suggestion.get('status')!='prepared':return
        link=browser_view_link(self.config,suggestion['id'])
        site=browser_login.site(urllib.parse.urlsplit(page['url']).hostname)
        mine=[a for a in actions if a.get('kind')=='open' and same_site(urllib.parse.urlsplit(a.get('url') or '').hostname,page['url'])]
        for item in mine:
            item.update(browser=True,site=site)
            if link:item['url']=link
        if not mine and page['worked']:
            extra['browser_view']={'label':'View in browser','site':site}
            if link:extra['next_actions']=[*actions,{'kind':'open','label':'View in browser','url':link,'browser':True,'site':site,'revision':'browser-view'}]

    def page_open(self, page):
        """Whether a task's page (task_page) is open in the Machine's browser now: its own tab (by DevTools ID, while the
        run did not close it), else a tab on that same address. The open tabs are read at most every TAB_LOOK seconds,
        for all cards at once; a browser that can't be reached has none open."""
        base=(browser_login.endpoints(self.config) or [None])[0]
        if not base:return False
        look=self.__dict__.setdefault('tab_look',{'at':None,'base':None,'tabs':[]})
        if look['at'] is None or look['base']!=base or time.monotonic()-look['at']>=TAB_LOOK:
            try:
                tabs=[{'id':t.get('id'),'url':t.get('url') or ''} for t in browser_login.browser_cdp._http(base,'/json/list',timeout=2) if t.get('type')=='page']
            except (browser_login.browser_cdp.CdpError,OSError,TypeError,AttributeError,ValueError):
                tabs=[]
            look.update(at=time.monotonic(),base=base,tabs=tabs)
        mine=page.get('target') and urllib.parse.urlsplit(base).port==page.get('port')
        return any(mine and t['id']==page['target'] or t['url']==page['url'] for t in look['tabs'])

    def task_pages(self, db, suggestion_id):
        """task_page, kept per run and number of steps: a finished run's steps don't change, and every card refresh asks."""
        try:
            key=db.execute("SELECT p.job_id,(SELECT count(*) FROM preparation_calls c WHERE c.job_id=p.job_id),(SELECT count(*) FROM preparation_runs r WHERE r.suggestion_id=p.suggestion_id) "
                           "FROM preparations p WHERE p.suggestion_id=?",(suggestion_id,)).fetchone()
        except sqlite3.OperationalError:
            return None
        key=(suggestion_id,*tuple(key or ()))
        cache=self.__dict__.setdefault('task_page_cache',{})
        if key not in cache:
            if len(cache)>500:cache.clear()
            cache[key]=task_page(db,suggestion_id)
        return cache[key]

    def chat_linked_files(self, db, suggestion_id):
        return chat_linked_files(db, suggestion_id)

    def result_document(self, suggestion_id, relative):
        with self.connect() as db:
            suggestion=db.execute('SELECT * FROM suggestions WHERE id=?',(suggestion_id,)).fetchone()
            linked = [f['path'] for f in self.suggestion_result(dict(suggestion),db)['result_files']] if suggestion else []
            if suggestion and relative not in linked:
                linked += [f['path'] for f in self.chat_linked_files(db, suggestion_id)]
            if not suggestion or relative not in linked:
                raise OwnerError('This result is not linked to that task')
        candidate=(WORKSPACE/relative).resolve()
        if not candidate.is_relative_to((WORKSPACE/'memory/assistant').resolve()):
            raise OwnerError('Result is outside the assistant folder')
        if candidate.stat().st_size>5*1024*1024:
            raise OwnerError('This result is too large to preview')
        return candidate

    def review_run_view(self, db, run):
        return review_run_view(db, run)

    def card_views(self, db, cards, jobs=True):
        """What the dashboard shows on cards beyond their row: the status payload and the Done pages alike. jobs=False
        does the first half (labels, people, feedback); jobs=True the rest (preparations, results). Kept by CARDS."""
        have = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        tables = tuple(t for t in CARD_TABLES if t in have)
        at = stamps.stamp(db, tables) if cards else None
        if at is None:
            return self._card_views(db, cards, jobs)
        inputs = [jobs, cards, sorted(self.owner_user_ids or ()), [a.get('service', 'gmail') for a in getattr(self, 'accounts', None) or []],
                  getattr(self, 'preparation_holds', None) if jobs else None, str(self.path), int(time.time() // CARD_KEEP_S)]
        key = hashlib.blake2b(json.dumps(inputs, sort_keys=True, default=str).encode(), digest_size=16).digest()
        built = []

        def build():
            before = copy.deepcopy(cards)  # a later pass may change what an earlier one added
            self._card_views(db, cards, jobs)
            built.append(1)
            return copy.deepcopy([{k: v for k, v in c.items() if k not in b or b[k] != v} for c, b in zip(cards, before)])
        kept = CARDS.get(key, (tables, at), build)
        if not built:
            for card, added in zip(cards, copy.deepcopy(kept)):
                card.update(added)

    def _card_views(self, db, cards, jobs):
        if not jobs:
            source_lines_shown(db, cards)  # a Slack DM by the person's name, never a raw chat handle
            source_marks(db, cards)  # the line's icon is the named message's own
            based_on_views(db, cards)  # "Based on Sam in #ops": the teammate's input the draft follows, with its link
            self.machine_fix_views(db, cards)  # a to-do from the computer's logs with a safe fix offers Do it
            labels = {r['suggestion_id']: skill_labels(r) for r in db.execute("SELECT suggestion_id,target_id,target_name FROM skill_clusters WHERE status IN ('pending','declined')")}
            for card in cards:
                if card['id'] in labels:
                    card['labels'] = labels[card['id']]
            # Written requests belong on the card too, even after preparation
            # or a later button click, and beyond the recent-feedback limit.
            # Which cards have any: one read for all, then only theirs are looked up (was one read per card)
            with_feedback = {r[0] for r in db.execute(
                "SELECT DISTINCT suggestion_id FROM decisions WHERE suggestion_id IN (SELECT value FROM json_each(?)) AND trim(feedback)<>'' "
                "AND source IN ('telegram','dashboard') AND id NOT IN (SELECT decision_id FROM decision_annotations)", (json.dumps([c['id'] for c in cards]),))}
            projects = {}  # a project's chip, read once per name
            for suggestion in cards:
                if looks_done(suggestion):  # where it sits in Done, among the closed ones (dashboard doneAt)
                    suggestion['looks_done_at'] = looks_done_at(db, suggestion)
                try:  # who it's about (its chip, also on a done to-do), and their weight to rank open cards by
                    suggestion['people'], weight = graph.card_people(db, json.loads(suggestion['event_ids'] or '[]'))
                    suggestion['source_line'] = lookalike.source_line(suggestion.get('source_line'), suggestion['people'])  # never the borrowed name
                    if suggestion['status'] not in todo_states.CLOSED:
                        suggestion['weight'] = weight
                except (sqlite3.Error, ValueError, TypeError):
                    pass
                if suggestion['status'] in gap_note.OPEN_STATUSES and suggestion.get('people'):
                    try:  # one short line on what isn't known about them, only where it helps (gap_note.card_gap)
                        gap = gap_note.card_gap(gap_note.for_card(db, json.loads(suggestion['event_ids'] or '[]'),
                                                                  [a.get('service', 'gmail') for a in getattr(self, 'accounts', None) or []],
                                                                  lambda e: own_message(e, self.owner_user_ids), now(), suggestion['id'], limit=1))
                        if gap:
                            suggestion['gap'] = gap
                    except (sqlite3.Error, ValueError, TypeError, KeyError):
                        pass
                if suggestion.get('project'):  # its project's page, for the chip on the to-do
                    try:
                        if suggestion['project'] not in projects:
                            projects[suggestion['project']] = graph.card_project_view(db, suggestion['project'])
                        suggestion['project_node'] = projects[suggestion['project']]
                        org = todo_org.project_org_view(db, suggestion['project_node'])  # one the owner or a review set
                        if org:
                            suggestion['project_node'] = {**suggestion['project_node'], 'org': org}
                    except sqlite3.Error:
                        pass
                # The organization it is about, in the review's word (CardsStore.suggest org), for its chip; org_said: a review
                # gave that word, also "none". Else the project's organization the owner or a review set (project_node org); never a
                # person's employer.
                suggestion['org_said'] = suggestion.get('org') is not None
                if suggestion.get('org'):
                    try:
                        found = todo_org.card_org_view(db, suggestion['org'])
                        if found:
                            suggestion['org_node'] = found
                    except sqlite3.Error:
                        pass
                if suggestion.get('next_action'):
                    suggestion['next_action']=json.loads(suggestion['next_action'])
                prompt=suggestion.get('feedback_request_id') and db.execute('SELECT status,error FROM feedback_prompts WHERE request_id=?',(suggestion['feedback_request_id'],)).fetchone()
                if prompt:suggestion['change_prompt']=dict(prompt)
                feedback = suggestion['id'] in with_feedback and db.execute("SELECT id,feedback,choice,created_at,source FROM decisions WHERE suggestion_id=? AND trim(feedback)<>'' AND source IN ('telegram','dashboard') AND id NOT IN (SELECT decision_id FROM decision_annotations) ORDER BY created_at DESC,rowid DESC LIMIT 1", (suggestion['id'],)).fetchone()
                suggestion['latest_feedback'] = dict(feedback) if feedback else None
                asked = feedback and db.execute('SELECT questions FROM decision_asks WHERE decision_id=?', (feedback['id'],)).fetchone()
                if asked:  # it answers the to-do's question(s): `asked` says which, `feedback` is the answer alone
                    suggestion['latest_feedback']['asked'] = json.loads(asked['questions'])
            for sid, files in chat_files.of_cards(db, [c['id'] for c in cards if c.get('origin') == 'owner']).items():
                next(c for c in cards if c['id'] == sid)['files'] = files  # what the owner made it with (New to-do)
            for sid, photos in whatsapp_images.of_cards(db, {'database': str(self.path)}, cards).items():
                next(c for c in cards if c['id'] == sid)['photos'] = photos  # a WhatsApp photo it came from (whatsapp_images.py)
            recurring.annotate(db, cards, timeutil.clock(local_tz()).date())  # "Repeats monthly" (recurring.py)
            calendar_clashes.annotate(db, cards)  # the other side of a calendar clash, for the owner only (calendar_clashes.py)
            still_needed.annotate(db, cards, now(), local_tz())  # "Still needed?" on a to-do untouched for a week (still_needed.py)
            return
        few = len(cards) <= 200  # a Done page: only its own; the status payload: all at once
        # shown: its status as every view shows it, a stuck run that a Claude Code or Codex job took over after it is not
        # Stuck any more (agent_jobs.shown_preparation)
        found={r['suggestion_id']:shown_job(dict(r)) for r in db.execute(f'SELECT p.*,{agent_jobs.shown_preparation(db)} shown,d.choice cause FROM preparations p LEFT JOIN decisions d ON d.id=p.decision_id'
                                                              +(' WHERE p.suggestion_id IN ('+','.join('?' for _ in cards)+')' if few else ''),[c['id'] for c in cards] if few else [])} if cards else {}
        pre=self.card_reads(db,cards)
        for suggestion in cards:
            job=found.get(suggestion['id'])
            # A run's questions are the to-do's only while that run waits on them (blocked, by its own word). Once a newer
            # message updated the to-do (update_card), the owner answered or the run went on, they are an older run's and
            # no view shows them: the row keeps them, the to-do doesn't ask them.
            asks=bool(job) and job['status']=='blocked' and not job['error']
            if job: suggestion.update(preparation_status=job['status'],preparation_reason=job['reason'],preparation_error=job['error'],
                                      preparation_details=job['details'],preparation_started_at=job['started_at'],preparation_retried=job['auto_retries']>0,
                                      preparation_questions=blocker_questions(job.get('questions')) if asks else [],
                                      preparation_no_questions=asks and job.get('questions')=='[]',
                                      preparation_cause=job.get('cause'),preparation_signed_in=str(job['decision_id']).startswith('signed-in:'),
                                      preparation_move_to=job.get('move_to') if job['status']=='blocked' else None,
                                      preparation_use=use_view(db,job.get('use_events')) if job['status']=='blocked' else None,
                                      preparation_connect=job.get('connect') if job['status']=='blocked' and not job['error'] else None,
                                      preparation_hold=getattr(self,'preparation_holds',{}).get(suggestion['id']) if job['status']=='queued' else None)
            suggestion.update(self.suggestion_result(suggestion, db, pre))

    def card_reads(self, db, cards):
        return card_reads(db, cards)

    def done_rows(self, db, titles=False):
        """Every done or dismissed card, the latest closed first, with its scope: light rows to count, filter and page.
        titles: also each one's title and who its messages went to (card_recipients), for a search."""
        rows = db.execute("SELECT s.id," + ("s.title,s.next_action," if titles else "") + "s.account_ids,s.area,coalesce((SELECT max(d.created_at) FROM decisions d WHERE d.suggestion_id=s.id AND d.choice IN ('complete','reject')),s.created_at) closed_at "
                          f"FROM suggestions s WHERE s.status IN {todo_states.sql(todo_states.CLOSED)} ORDER BY closed_at DESC,s.id").fetchall()
        return [{'id': r['id'], 'title': (r['title'] or '') if titles else '', 'who': card_recipients(r['next_action']) if titles else '', 'closed_at': r['closed_at'],
                 'scope': suggestion_scope(r['account_ids'], self.accounts, r['area']) if getattr(self, 'accounts', None) and r['account_ids'] is not None
                 and not todo_areas.machine_own(r['account_ids'], self.accounts, r['area']) else None} for r in rows]

    def done_counts(self, db):
        rows = self.done_rows(db)
        return {'all': len(rows), 'work': sum(r['scope'] == 'work' for r in rows), 'personal': sum(r['scope'] == 'personal' for r in rows)}

    def done_page(self, cursor=0, limit=30, query='', scope='', only=''):
        """A page of the Done list, the latest closed first, for the main pane and the sidebar; query matches card titles
        and who its messages went to (every done card, not only the ones loaded), scope is work or personal; only: that one
        card (a link from Activity)."""
        offset, limit = max(0, int(cursor or 0)), max(1, min(int(limit), 50))
        words = [w for w in str(query or '').casefold().split() if w]
        with self.connect() as db:
            rows = [r for r in self.done_rows(db, titles=bool(words)) if (scope not in ('work', 'personal') or r['scope'] == scope)
                    and all(w in (r['title'] + ' ' + r['who']).casefold() for w in words) and (not only or r['id'] == only)]
            ids = [r['id'] for r in rows[offset:offset + limit]]
            by_id = {r['id']: dict(r) for r in db.execute('SELECT * FROM suggestions WHERE id IN (' + ','.join('?' for _ in ids) + ')', ids)} if ids else {}
            cards = [by_id[i] for i in ids if i in by_id]
            closed = {r['id']: r for r in rows[offset:offset + limit]}
            self.card_views(db, cards, jobs=False)
            self.card_views(db, cards, jobs=True)
            following = follow_ups.cards_view(db, ids)  # sent and skipped follow-ups fold into one row per board and day
            for card in cards:
                card['closed_at'] = closed[card['id']]['closed_at']
                if card['id'] in following:
                    card['follow_up'] = following[card['id']]
                if closed[card['id']]['scope']:
                    card['scope'] = closed[card['id']]['scope']
        return {'cards': cards, 'next': str(offset + limit) if len(rows) > offset + limit else None, 'total': len(rows)}

    def snapshot(self, accounts, done=100, lean=False, connectors=True):
        """The status. lean: without the dashboard's heaviest parts (promises, recent review runs, the quality report,
        the missed-work audit), for an agent's compact status (compact_status), which never reads them: a review asks
        for it on a busy Machine, where the whole status took longer than the tool's 30 seconds. connectors=False: an
        empty list for them (the dashboard's status makes them apart, connector_views)."""
        promises = [] if lean else self.promises()
        with self.connect() as db:
            result = {table: [dict(r) for r in db.execute('SELECT * FROM ' + table + ' ORDER BY ' + column + ' DESC LIMIT 100')]
                      for table, column in [('suggestions', 'created_at'), ('decisions', 'created_at'), ('analyses', 'started_at')]}
            result['promises'] = promises
            annotations={r['decision_id']:r for r in db.execute('SELECT decision_id,status,reason,superseded_by FROM decision_annotations WHERE decision_id IN (SELECT value FROM json_each(?))',
                                                                 (json.dumps([d['id'] for d in result['decisions']]),))}  # one read, not one per decision
            for decision in result['decisions']:
                annotation=annotations.get(decision['id'])
                if annotation:
                    decision.update(annotation={k:annotation[k] for k in ('status','reason','superseded_by')},feedback='')
            # Each decision carries its to-do's title: an older done to-do is past the suggestions list below, and
            # Learning, Decisions showed its id instead.
            ids = sorted({d['suggestion_id'] for d in result['decisions'] if d.get('suggestion_id')})
            titles = {r['id']: r['title'] for r in db.execute('SELECT id,title FROM suggestions WHERE id IN (' + ','.join('?' for _ in ids) + ')', ids)} if ids else {}
            for decision in result['decisions']:
                decision['title'] = titles.get(decision['suggestion_id']) or ''
            # What was learned, newest first; a condensed one says how many notes it stands for (the owner can undo that).
            merged = {r['merged_into']: r['n'] for r in db.execute('SELECT merged_into,count(*) n FROM facts WHERE merged_into IS NOT NULL GROUP BY 1')}
            about = {}  # who each is about (fact_about), for About <name> with Not about them
            for r in db.execute('SELECT a.fact_id,a.node_id,n.name FROM fact_about a JOIN graph_nodes n ON n.id=a.node_id WHERE a.removed_at IS NULL ORDER BY a.created_at,a.node_id'):
                about.setdefault(r['fact_id'], []).append({'id': r['node_id'], 'name': r['name']})
            result['facts'] = [{**dict(r), 'merged': merged.get('fact:' + str(r['id']), 0), 'about': about.get(r['id'], [])} for r in
                               db.execute('SELECT id,text,suggestion_id,created_at,kind,fact_kind,valid_until,source,quote FROM facts WHERE removed_at IS NULL '
                                          'ORDER BY created_at DESC,id DESC')]
            # Facts that ended (past their end day) in the last 30 days, each the owner can bring back; and those set aside
            # as not used lately to make room (facts.py set_aside), the last 90 days, same Bring back.
            month = (dt.datetime.fromisoformat(now()) - dt.timedelta(days=30)).isoformat()
            result['facts_ended'] = [dict(r) for r in db.execute(
                "SELECT id,text,fact_kind,valid_until,removed_at,quote FROM facts WHERE merged_into='expired:'||id AND removed_at>=? ORDER BY removed_at DESC LIMIT 20", (month,))]
            result['facts_aside'] = [dict(r) for r in db.execute(
                "SELECT id,text,kind,fact_kind,removed_at,quote FROM facts WHERE merged_into='aside:'||id AND removed_at>=? ORDER BY removed_at DESC LIMIT 100",
                ((dt.datetime.fromisoformat(now()) - dt.timedelta(days=90)).isoformat(),))]
            result['voices'] = [{**v, 'merged': merged.get('voice:' + v['channel'], 0)} for v in self.voices(db)]
            result['learning_changes'] = learning_loop.recent(db)  # the learning loop's changes, each with Undo
            result['moved'] = [dict(r) for r in db.execute("SELECT substr(f.merged_into,7) skill_id,coalesce(k.name,'a skill') name,count(*) notes FROM facts f "
                                                           "LEFT JOIN skills k ON k.id=substr(f.merged_into,7) WHERE f.merged_into LIKE 'skill:%' GROUP BY 1,2")] \
                if db.execute("SELECT 1 FROM sqlite_master WHERE name='skills'").fetchone() else []
            last = db.execute("SELECT at FROM rule_changes WHERE kind='condense' AND text LIKE 'Condensed%' ORDER BY at DESC LIMIT 1").fetchone()
            if last:  # the latest pass: every note merged that day
                day = last['at'][:10]
                result['condensed'] = {'at': last['at'], 'notes': db.execute("SELECT count(*) FROM facts WHERE merged_into IS NOT NULL AND substr(removed_at,1,10)=?", (day,)).fetchone()[0]}
            # Keep outstanding items visible even after a long completed history.
            # The done ones: the `done` closed last (a to-do made weeks ago and sent just now is the newest done), each with
            # when it was closed, so Done starts with the one just finished; also every one closed in the last day (its
            # done report, Undo), up to 100. The dashboard asks for its Done list's first page (DONE_FIRST) and loads the
            # rest a page at a time (api/cards/done), an older one a link points to by itself: each done card is ~4 KB.
            day = dt.datetime.fromisoformat(now()) - dt.timedelta(days=1)

            def today(at):
                try:
                    return dt.datetime.fromisoformat(at) >= day
                except (TypeError, ValueError):
                    return True  # unreadable: kept, as before
            recent = {r['id']: r['closed_at'] for n, r in enumerate(self.done_rows(db)[:100]) if n < done or today(r['closed_at'])}
            result['suggestions'] = [dict(r) for r in db.execute(f"SELECT * FROM suggestions WHERE status NOT IN {todo_states.sql(todo_states.CLOSED)} OR id IN (SELECT value FROM json_each(?)) ORDER BY created_at DESC", (json.dumps(list(recent)),))]
            for card in result['suggestions']:
                if card['id'] in recent:
                    card['closed_at'] = recent[card['id']]
            self.card_views(db, result['suggestions'], jobs=False)
            # How many cards are done or dismissed, per scope: the Done lists' counts; they load the rest a page at a time
            result['done_counts'] = self.done_counts(db)
            result['clear_pace'] = clear_pace.seconds(db)  # seconds per action, the owner's own: To-dos' time to clear
            result['suggestion_counts'] = {r['status']: r['count'] for r in db.execute('SELECT status,count(*) count FROM suggestions GROUP BY status')}
            result['areas'] = todo_areas.areas(accounts)  # where a to-do can move (More, Move to)
            try:  # Connections, Disconnected lately (mail_grants.py receipts): one row per account, named (names.py)
                import mail_grants
                from machine import names
                result['disconnected'] = names.disconnected_rows(mail_grants.receipts(self.config)) if self.config.get('database') else []
            except Exception:  # noqa: BLE001 - never costs the status
                result['disconnected'] = []
            result['connectors'] = self.connector_views(db, accounts) if connectors else []
            # Newest first: the dashboard shows the top few and says when each happened.
            result['deliveries'] = [dict(r) for r in db.execute('SELECT * FROM deliveries ORDER BY updated_at DESC,rowid DESC')]
            self.card_views(db, result['suggestions'], jobs=True)
            # Automated follow-ups: which one a to-do is, and the board's grouped to-do it goes in (follow_ups.py)
            following = follow_ups.cards_view(db, [x['id'] for x in result['suggestions']])
            for x in result['suggestions']:
                if x['id'] in following:
                    x['follow_up'] = following[x['id']]
            # Follow-ups going out spaced, per board: "Sending 3 of 8…", then "Sent 8" (follow_ups.progress)
            result['follow_up_progress'] = follow_ups.progress(db, now())
            result['recurring_offer'] = recurring.offer_view(db)  # "Make this a recurring to-do?", once (recurring.py)
            result['routine_offer'] = routine_offers.view(db)  # "Turn on Newsletter cleanup?", once (routine_offers.py)
            counts = db.execute('SELECT count(*) total,sum(analyzed_version<version) pending,sum(analyzed_version=0) first_review,coalesce(sum(analyzed_version<version AND deferrals>=?),0) set_aside FROM events WHERE history=0', (SET_ASIDE_AFTER,)).fetchone()
            result['review_health'] = {**dict(counts), 'last_completed': db.execute("SELECT max(finished_at) FROM analyses WHERE status='complete'").fetchone()[0]}
            if counts['set_aside'] and not lean:  # the list under the count: what each is waiting for (review_last_look.py)
                result['review_health']['set_aside_list'] = review_last_look.listing(self, db)
            result['review_runs'] = []
            for row in db.execute('SELECT * FROM review_runs ORDER BY started_at DESC LIMIT ?', (1 if lean else 20,)):
                result['review_runs'].append(self.review_run_view(db, dict(row)))
            result['review_health']['worker'] = result['review_runs'][0] if result['review_runs'] else None
            listed = {review['id']: json.loads(review['items']) for review in result['analyses']}
            # each listed signal's review state in one read, not one per signal (thousands over the last 100 reviews)
            analyzed = {r[0]: r[1] for r in db.execute('SELECT id,analyzed_version FROM events WHERE id IN (SELECT value FROM json_each(?))',
                                                       (json.dumps(sorted({i['id'] for items in listed.values() for i in items})),))}
            for review in result['analyses']:
                items = listed[review['id']]
                review['checked_count'] = sum(not i.get('excluded') and not i.get('deferred') for i in items) if review['status']=='complete' else 0
                outstanding = sum(1 for item in items if item['id'] in analyzed and analyzed[item['id']] < item['version'])
                review['remaining_count'] = outstanding
                review['recovered_count'] = sum(not i.get('excluded') for i in items) - outstanding if review['status']!='complete' else None
        if lean:
            return result
        result['quality'] = self.quality_report()
        result['missed_work'] = missed_work.status(self.connect)  # the weekly missed-work audit (missed_work.py)
        notes = bring_in.status(self.connect)  # lines of the owner's OpenClaw notes worth keeping (bring_in.py)
        if notes:  # nothing to bring in: nothing in the status, so nothing on the page
            result['bring_in'] = notes
        return result

    def connector_views(self, db, accounts):
        """Each connection's card on Connections: its sync state, reads and counts. Apart from the rest of the snapshot,
        as these change with each sync round and the rest mostly doesn't (StatusApp.status_kept)."""
        out = []
        for account in accounts:
            row = db.execute('SELECT * FROM checkpoints WHERE account_id=?', (account['id'],)).fetchone()
            cutoff = (dt.datetime.fromisoformat(now()) - dt.timedelta(hours=24)).isoformat()
            # The card's total is everything kept from this source, history included (docs/help/history.md), from
            # events_account_time alone; last 24h and not checked stay new signals only, from events_signal_counts.
            counts = db.execute('SELECT (SELECT count(*) FROM events WHERE account_id=?1) total,sum(analyzed_version<version) pending,'
                                'sum(ingested_at>=?2) signals_24h FROM events WHERE account_id=?1 AND history=0',
                                (account['id'], cutoff)).fetchone()
            state = json.loads(row['state']) if row else {}
            channel_health = {}
            if account.get('service') == 'android':
                feed = db.execute('SELECT last_checked,last_recorded,error FROM android_feed_health WHERE id=1').fetchone()
                channel_health = {'transport':account.get('transport'), 'feed_health':dict(feed) if feed else None}
            if account.get('service') == 'whatsapp' and not account.get('shared'):  # Read photos (whatsapp_images.py)
                channel_health = {'photos': whatsapp_images.view(db, account), 'history': whatsapp_history(account)}
            if account.get('service') == 'slack':
                channels = state.get('channels', [])
                channel_health = {'conversations': len(channels),
                                  'conversations_collected': sum(bool(c.get('last_scan')) for c in channels),
                                  'deferred_threads': sum(bool(c.get('deferred_thread')) for c in channels),
                                  'conversation_errors': sum(bool(c.get('error')) for c in channels),
                                  'first_import': slack_first_import_progress(state)}
            if account.get('service') == 'salesflare':  # its round of accounts, what it set aside, Stop and Restart
                channel_health = {'salesflare': salesflare_progress(account, state)}
            if account.get('service') == 'salesforce':  # Update contact details: on or off, and what it updated last
                channel_health = {'crm_sync': crm_sync_health(account, state)}
            if account.get('service') == 'intercom':  # who a reply goes out as, after the owner's Send; none: it only reads
                channel_health = {'replies_as': (account.get('reply_admin_name') or 'you') if next_actions.intercom_replies_on(account) else ''}
            if account.get('service') == 'teams':  # what it can't read yet and why: admin, license or blocked (connectors/teams.py)
                channel_health = {'teams_missing': dict(state.get('missing') or {})}
            if account.get('service') == 'docs':  # Google or Microsoft, and whether an approved reply can be posted
                channel_health = docs_health(self.config, account, state)
            if account.get('service') in CALENDAR_SERVICES:  # its card counts events coming up, not mail (Next 7 days)
                # status is counted in SQL (a plain key, message_seal.ROUTING_KEYS). A row sealed before it was one shows
                # no status beside its sealed member until machine/store/plain_keys.py has been over it: those are read
                week = (account['id'], now(), (dt.datetime.fromisoformat(now()) + dt.timedelta(days=7)).isoformat())
                coming = 'FROM events WHERE account_id=? AND deleted=0 AND occurred_at>=? AND occurred_at<? AND '
                unseen = "json_extract(metadata,'$.status') IS NULL AND json_extract(metadata,'$.mc1_sealed') IS NOT NULL"
                channel_health = {'upcoming_7d': db.execute(
                    f"SELECT count(*) {coming} COALESCE(json_extract(metadata,'$.status'),'')!='cancelled' AND NOT ({unseen})", week).fetchone()[0] + sum(
                    (json.loads(m or '{}').get('status') or '') != 'cancelled' for (m,) in db.execute(f'SELECT metadata {coming} {unseen}', week))}
            activity = [dict(r) for r in db.execute('SELECT at,status,signals,error,retry_at FROM sync_activity WHERE account_id=? ORDER BY at DESC,rowid DESC LIMIT 12',(account['id'],))]
            last_failure = db.execute("SELECT at,error FROM sync_activity WHERE account_id=? AND status='failed' ORDER BY at DESC,rowid DESC LIMIT 1",(account['id'],)).fetchone()
            failures_24h = db.execute("SELECT count(*) FROM sync_activity WHERE account_id=? AND status='failed' AND at>=?",(account['id'],cutoff)).fetchone()[0]
            out.append({'sync_activity':activity,'last_failure':dict(last_failure) if last_failure else None,
                        'failures_24h':failures_24h,'id': account['id'], 'email': account.get('email', ''), 'boundary': account['boundary'],
                        'boundary_by': account.get('boundary_by'),
                        'service': account.get('service', 'gmail'),
                        **({'last': True} if groups.last(account.get('service', 'gmail')) else {}),  # a catch-all: after the others
                        'group': source_group(account.get('service', 'gmail')),  # its + Add group, which picks its tab
                        'poll_seconds':account.get('poll_seconds',300),
                        'read_window': read_window(account),
                        'display_name': names.account_name(account, accounts, UNNAMED.get(account.get('service'))),
                        # a Fleet share the owner also connected themselves rests (shared_connectors.covered_by)
                        'covered_by': covered_name(accounts, account),
                        **(dict(row) if row else {}), **dict(counts), **channel_health,
                        **(silent_failure(db, account, row) or {}), 'backfill': history_store.progress(db, [account['id']]).get(account['id'])})
        return out
