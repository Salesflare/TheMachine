"""Everything a Machine knows, by part: the one list that an export, an import and any other way out (a portable copy
for another AI, say) read from, so none of them misses a table, a folder or a conversation (docs/moving.md).

- PARTS: the parts an export's manifest lists, in the owner's words.
- TABLES: every table The Machine creates, with its part. tests/test_export_complete.py fails when the code creates a
  table that is not in it, so a new table can't be left out of an export by accident.
- DATA_FILES: what sits in the data folder by name, with its part (the whole folder moves; this only names it).
- HOME_AREAS: what lives outside the data folder, under the home folder (OpenClaw's conversations, the send logs).
- NOT_EXPORTED: what can't move, and why. An export's manifest carries it, with what is true on that install.

Reading:
- databases(config_path): the SQLite files of an install, [(name, path)].
- rows(path, table, key): one table's rows as dicts, opened (sealed message text in the clear), streamed.
- walk(config_path, ...): one iterator over everything, [Item]: each row of each table, each file. It reads, never
  writes, and holds one row or one file name at a time, so it runs on a small hosted Machine too.
- digest(db, table): (rows, sha256) of a table in a stable order: what the manifest lists and an import checks."""
import base64
import hashlib
import json
import os
import re
import sqlite3
from contextlib import closing
from pathlib import Path

PARTS = {
    'messages': 'Messages from all sources',
    'conversations': 'Conversations with your AI',
    'todos': 'To-dos, with their history and events',
    'drafts': 'Drafts, sends and their undo history',
    'decisions': 'Decisions',
    'promises': 'Promises',
    'memories': 'Memories and what it learned about people',
    'preferences': 'Learned preferences',
    'graph': 'The Graph: people, organizations and projects',
    'skills': 'Skills',
    'agents': 'Agent jobs, their transcripts and work folders',
    'attachments': 'Attachments and photos',
    'sharing': 'Fleet, Network and sharing',
    'activity': 'Activity and history',
    'settings': 'Configuration',
    'workspace': "Your AI's workspace (memory notes, USER.md)",
    'index': 'Search and similarity indexes',
}


def _names(text):
    return text.split()


# Every table The Machine creates (CREATE TABLE in the code), by part. An index (search, similarity) is exported too:
# rebuilding it would cost hours on a big mailbox.
_BY_PART = {
    'messages': _names('''events checkpoints sync_activity sync_daily history_backfill android_inbox
        android_receipts android_feed_health chats messages state outbox signal_state signal_chats signal_messages signal_outbox photo_asks email_bounce_events email_bounce_scan email_bounce_cc email_bounce_cc_scan
        email_bounces own_addresses own_address_choices own_address_fetched own_domains slack_members meet_links meet_log
        meet_pins meet_seen meet_sessions meet_prefs meeting_moves talk_lines moved_in'''),
    'todos': _names('''suggestions suggestion_keys card_moves card_uses decision_asks analyses review_runs review_save_failures first_look_ahead feedback_prompts
        recaps recap_items thread_snoozes slipped milestones chat_stops preparations preparation_runs preparation_calls
        recurring_cards recurring_offers recurring_series routines routine_offers routine_runs routine_changes mail_cleanup_items mail_cleanup_senders facebook_birthdays digest_items digest_spend task_pages follow_up_advice follow_up_basis follow_up_cards
        follow_up_changes follow_up_ends follow_up_holds follow_up_pace follow_up_pauses follow_up_rules follow_up_threads
        missed_audits missed_audit_items missed_audit_calibration review_misses project_success project_success_checks project_stall_runs project_stall_items calendar_clashes meeting_preps gateway_starts'''),
    'drafts': _names('''draft_edits draft_saves draft_seen deliveries action_jobs calendar_writes meeting_writes handoff_mails
        follow_up_sends merge_effects edits_offered'''),
    'decisions': _names('decisions decision_annotations tool_approval_proposals'),
    'promises': _names('promises promise_log'),
    'memories': _names('''facts fact_about bring_in_items bring_in_lines bring_in_state person_summaries person_summary_runs gbrain_meta gbrain_notes gbrain_pages
        note_kinds memory_use'''),
    'preferences': _names('''learned_fixes learning_changes learning_signals learning_state rule_changes voices voice_merges voice_prefs
        pacing_prefs pacing_starts security_prefs enrich_prefs notify_prefs error_feed_prefs handoff_mail_prefs
        whatsapp_photo_prefs team_learning_prefs digest_interests'''),
    'graph': _names('''graph_nodes graph_identifiers graph_edits graph_events graph_history graph_history_events graph_imports graph_links graph_merges graph_names graph_offers
        graph_org_asks graph_relations graph_resources graph_role_asks graph_same graph_state graph_unnamed manual_nodes
        hidden_domains identity_names forgotten_people forgotten_salt owner_numbers person_edits person_facts person_orgs
        person_photo_tries person_photos person_profiles person_roles role_corrections org_aliases org_apart org_edits
        org_profiles org_logo_retries org_logo_tries projects project_moves project_org_backfill project_org_checks project_org_fills
        project_splits project_people event_projects boards board_backfill_asks board_backfills board_backfills_queued board_fit_undo
        board_fits board_offers board_suggestions side_changes side_rule self_record_backups crm_fields crm_tags crm_values
        record_changes record_owners contact_photo_links contact_photo_runs reconnect_asks ms_photo_asks ms_photo_accounts telegram_photo_asks whatsapp_photo_asks mail_hidden
        mail_shown'''),
    'skills': _names('skills skill_hints skill_task_decided skill_clusters help_topics'),
    'agents': _names('''agent_jobs agent_result_receipts agent_key_pins agent_relayed chat_models chat_fast_sessions'''),
    'attachments': _names('chat_files whatsapp_photos'),
    'sharing': _names('''fleet_briefs fleet_claims fleet_handled fleet_in fleet_log fleet_meta fleet_notices fleet_out
        fleet_rules fleet_scopes fleet_requests fleet_splits fleet_reviews fleet_learnings fleet_learn_read
        fleet_learn_removed fleet_learn_seen fleet_learn_used fleet_learn_vectors network_aliases network_outbox network_pins
        network_replies network_sealed network_taken network_twins network_request_nodes network_looked network_people
        share_lines share_meta share_out share_people share_private share_rules share_threads team_asks team_blobs
        team_files team_mail team_pending team_records team_sources team_wants team_learnings team_learning_votes
        contact_shares contact_marks family_invite_log family_invite_offers ai_clients ai_codes ai_connections ai_tokens
        ai_folded ai_writes ai_activity'''),
    'activity': _names('''activity_accounts activity_blocks activity_seen faults fault_versions error_feed retention_runs
        store_fixes plain_key_pass data_stamps profile_runs notify_queue notify_digests notify_app_lines notify_app_devices push_subscriptions'''),
    'index': _names('event_search event_vectors event_passages event_vector_skips fact_vectors fact_search'),
}
TABLES = {table: part for part, names in _BY_PART.items() for table in names}

# SQLite's own bookkeeping and an FTS index's inner tables: copied with their database, never counted on their own
INNER = re.compile(r'^sqlite_|_(?:data|idx|docsize|config|content)$')

# The data folder by name (the whole folder moves; files are found by walking it). Keys are kept apart (moving.plan).
DATA_FILES = {
    'config.json': 'settings', 'events.sqlite': 'messages', 'telegram.sqlite': 'messages', 'telegram': 'messages', 'signal': 'messages', 'chat-files': 'attachments',
    'attachments': 'attachments', 'whatsapp-photos': 'attachments', 'open-attachments': 'attachments',
    'agent-jobs': 'agents', 'prompt-receipts': 'activity', 'voice': 'preferences', 'signatures.json': 'preferences',
    'notes.txt': 'memories', 'slack-rounds.json': 'messages', 'bug-queue.json': 'activity', 'bug-offers.json': 'activity',
    'integrations': 'settings', 'connectors': 'settings', 'git': 'settings',
}

# Under the home folder, outside the data folder: (path relative to home, part, what it is). Files there move along
# and come back to the same place; OpenClaw's databases are merged with the new install's sign-ins (moving.py).
HOME_AREAS = [
    ('.openclaw/agents/*/agent/openclaw-agent.sqlite', 'conversations', "Your AI's conversations, memory index and goals"),
    ('.openclaw/agents/*/sessions', 'conversations', "Your AI's conversation transcripts"),
    ('.openclaw/agents/*/agent/workshop-skills', 'skills', 'skills made in the workshop'),
    ('.openclaw/state/openclaw.sqlite', 'conversations', "Your AI's scheduled jobs, plugin memory and state"),
    ('.openclaw/media/inbound', 'attachments', 'photos and files sent to your AI'),
    ('.openclaw/media/outbound', 'attachments', 'photos and files your AI sent'),
    ('.openclaw/media/tool-image-generation', 'attachments', 'images your AI made'),
    ('.local/share/x-inbox/sends.jsonl', 'drafts', 'what was sent on X, so nothing goes twice'),
    ('.local/share/linkedin-inbox/sends.jsonl', 'drafts', 'what was sent on LinkedIn, so nothing goes twice'),
    ('.cache/the-machine/fixes', 'todos', 'self-fixes being prepared'),
]

# OpenClaw's own tables that hold sign-ins and keys: they stay out of an export without keys, and an import keeps the
# new install's own (moving.py)
OPENCLAW_SECRET = re.compile(r'secret|auth_profile|apns|identity_key|revision_key|token|credential|device_pair|pairing_request')

# What can't move, and why. `after` is what the owner does after an import.
NOT_EXPORTED = [
    {'what': 'Sign-ins to Google and Microsoft through the hosted service', 'why': 'they belong to the hosting and only work there',
     'after': 'Sign in to Google or Microsoft again'},
    {'what': 'Your AI plan sign-in (ChatGPT, Claude) and API keys', 'why': 'the providers tie these to one computer or the export leaves them out',
     'after': 'Sign in to ChatGPT or Claude again, or paste your API key'},
    {'what': "WhatsApp's device link", 'why': 'WhatsApp links one device at a time; a copy would not work',
     'after': 'Link WhatsApp again with the QR code. Your messages are kept'},
    {'what': 'Telegram, Slack and other source tokens', 'why': 'keys and tokens come along only when you include them',
     'after': 'Connect those sources again'},
    {'what': 'AI connections (ChatGPT and Claude connectors)', 'why': 'their access tokens are for the old address',
     'after': 'Connect them again in Settings'},
    {'what': 'Phone notifications', 'why': 'each phone signs up with one Machine', 'after': 'Open the app on your phone once'},
    {'what': 'Conversations you deleted', 'why': 'They are kept for a while, but they are deleted', 'after': ''},
    {'what': 'Installed programs, caches and browser sessions', 'why': 'any computer rebuilds them', 'after': ''},
    {'what': 'The Machine Network identity, without keys', 'why': 'it is a key',
     'after': 'Teammates and friends see a key-change notice once'},
]
NOT_EXPORTED_HOME = [
    ('.openclaw/agents/*/agent/codex-home', "Codex's own sign-in and caches for your AI"),
    ('.openclaw/media/browser', 'browser screenshots, a cache'),
    ('.openclaw/media/playback-transcode', 'audio converted for playback, a cache'),
    ('.openclaw/browser', 'browser profiles: sign-ins tied to this computer'),
    ('.local/share/wacli', "WhatsApp's device link and its own copy of your chats (your messages are in the export)"),
    ('.openclaw/credentials', 'keys; included only with keys'),
    ('.claude/.credentials.json', "Claude Code's sign-in, tied to this computer (only its date is read, to notice a new sign-in)"),
]

DATA_HOME = '.local/share/personal-assistant'  # the data folder's usual place: exported whole, whatever is in it

# Other places under the home folder the code uses, and why an export does not need them as they are
HOME_OTHER = {
    '.openclaw/openclaw.json': "Your AI's settings with its keys: included only with keys",
    '.openclaw/workspace': 'exported as the workspace part',
    '.openclaw': "OpenClaw's folder: its parts are listed one by one",
    '.local/share': 'where the data folder sits',
    '.local/bin': 'installed programs',
    '.local/state/x-inbox/run.lock': 'a lock file',
    '.cache': 'caches',
    '.codex': "Codex's own folder: the transcripts of agent jobs are exported, its sign-in is not",
    '.claude': "Claude Code's own folder: the transcripts of agent jobs are exported, its sign-in is not",
    'Library/Application Support/gogcli/keyring': 'Google sign-in keys: included only with keys',
    '.config/the-machine-release/signing-key': 'the release signing key of The Machine itself, not yours',
    '.config/linkedin-inbox/query-ids.json': "LinkedIn's page ids, found again by itself",
}


def part_of(table):
    return TABLES.get(table) or ('index' if INNER.search(table) else 'other')


def databases(config_path):
    """The SQLite files in an install's data folder, [(name relative to it, path)], the main database first."""
    config_path = Path(config_path).expanduser()
    data = config_path.parent
    try:
        main = Path(json.loads(config_path.read_text()).get('database') or data / 'events.sqlite').expanduser()
    except (OSError, ValueError):
        main = data / 'events.sqlite'
    found = []
    for base, dirs, names in os.walk(data):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', '__pycache__', 'backups', 'backups-manual')]
        for name in names:
            path = Path(base) / name
            if path.suffix in ('.sqlite', '.db') and not path.is_symlink() and not re.search(r'\.(?:bak|backup)[-.]|\.before-|\.pre-', name):
                found.append((str(path.relative_to(data)), path))
    return sorted(found, key=lambda item: (item[1] != main, item[0]))


def tables(db):
    """A database's own tables, without SQLite's bookkeeping and an FTS index's inner tables, [(name, virtual)]."""
    out = []
    for name, sql in db.execute("SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name"):
        if name.startswith('sqlite_'):
            continue
        virtual = (sql or '').upper().startswith('CREATE VIRTUAL')
        if not virtual and INNER.search(name) and db.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? AND sql LIKE 'CREATE VIRTUAL%'", (re.sub(INNER, '', name),)).fetchone():
            continue
        out.append((name, virtual))
    return out


def _plain(value):
    if isinstance(value, (bytes, memoryview)):
        return {'b64': base64.b64encode(bytes(value)).decode()}
    return value


def quoted(name):
    """A table or column name as an SQL identifier. Names come from sqlite_master, and on an import from the archive,
    so a quote in one never ends the identifier early."""
    return '"' + str(name).replace('"', '""') + '"'


def _order(db, table):
    """A stable order for a table's rows: its rowid, or its primary key for a table without one."""
    info = db.execute('PRAGMA table_info(' + quoted(table) + ')').fetchall()
    keys = [r[1] for r in sorted((r for r in info if r[5]), key=lambda r: r[5])]
    without_rowid = 'WITHOUT ROWID' in (db.execute("SELECT sql FROM sqlite_master WHERE name=?", (table,)).fetchone()[0] or '').upper()
    return ','.join(quoted(k) for k in (keys if without_rowid and keys else [])) or 'rowid'


def connect(path, key=None):
    """A read-only connection whose rows open sealed message text with the install's key (message_seal.py)."""
    import message_seal
    db = sqlite3.connect(f'file:{path}?mode=ro', uri=True, timeout=30, factory=message_seal.Connection)
    if key:
        message_seal.attach(db, message_seal.Sealer(key))
    else:
        db.row_factory = sqlite3.Row
    return db


def rows(db, table):
    """One table's rows as dicts, in a stable order, one at a time."""
    for row in db.execute('SELECT * FROM ' + quoted(table) + ' ORDER BY ' + _order(db, table)):
        yield {k: row[k] for k in row.keys()}


def digest(db, table):
    """(rows, sha256 hex) of a table's rows in a stable order, every value as written (blobs in base64)."""
    h, count = hashlib.sha256(), 0
    for row in db.execute('SELECT * FROM ' + quoted(table) + ' ORDER BY ' + _order(db, table)):
        h.update(json.dumps([_plain(v) for v in tuple(row)], ensure_ascii=False, default=str).encode() + b'\n')
        count += 1
    return count, h.hexdigest()


def file_digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


class Item(dict):
    """One thing walk() found: kind 'row' (part, db, table, row) or 'file' (part, path, name: where it sits in an export)."""
    __getattr__ = dict.get


def walk(config_path, workspace=None, openclaw_home=None, files=True, row_data=True):
    """Every row of every table and every file of an install, part by part, streamed. Message text comes opened with
    the install's key. Keys and tokens (moving.plan's secrets) are never in it. The rows of OpenClaw's databases are
    left to OpenClaw's own format; their files are listed."""
    import message_seal
    import moving
    config_path = Path(config_path).expanduser()
    for name, path in databases(config_path):
        key = message_seal.load_key(path)
        with closing(connect(path, key)) as db:
            for table, virtual in tables(db):
                if virtual:
                    continue
                part = part_of(table)
                if not row_data:
                    yield Item(kind='table', part=part, db=name, table=table)
                    continue
                for row in rows(db, table):
                    yield Item(kind='row', part=part, db=name, table=table, row=row)
    if not files:
        return
    for kind, path, entry in moving.plan(config_path, workspace, openclaw_home):
        if kind == 'secret' or kind == 'db':
            continue
        yield Item(kind='file', part=file_part(entry), path=path, name=entry)


def file_part(entry):
    """The part of a file by where it sits in an export (moving.plan's names)."""
    parts = Path(entry).parts
    if parts[0] == 'secrets':
        return 'settings'
    if parts[0] == 'workspace':
        return 'workspace'
    if parts[0] == 'config' or parts[0] == 'connectors':
        return 'settings'
    if parts[0] in ('home', 'openclaw'):
        rest = ('.openclaw/' if parts[0] == 'openclaw' else '') + '/'.join(parts[1:])
        for pattern, part, _ in HOME_AREAS:
            if re.match(re.escape(pattern).replace(r'\*', '[^/]+') + '(?:/|$)', rest):
                return part
        return 'other'
    if parts[0] == 'agents-home':
        return 'agents'
    if parts[0] == 'data' and len(parts) > 1:
        return DATA_FILES.get(parts[1]) or ('messages' if entry.endswith(('.sqlite', '.db')) else 'other')
    return 'other'
