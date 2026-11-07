"""The Store's core (refactor PR 13, the first Store step): opening the database, its schema (the DDL in __init__, as
is), message protection (sealing, the safety copy, restores) and the purges of excluded sources, connect and
checkpoint. assistant.py's Store subclasses StoreCore and keeps the rest of its methods until they move here by table
group (machine/store/ mixins, docs/code-map.md). Moved out of assistant.py as is."""
import contextlib
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sqlite3
import time

import activity
import activity_log
import ai_access
import bounces
import chat_files
import chat_model
import embeddings
import error_feed
import follow_ups
import graph
import handoff_mail
import learning_loop
from machine.config import LOG
from machine.sources.exclusions import calendar_title_excluded, email_subject_excluded, excluded_by_rules, routine_rules
from machine.store import history as history_store
from machine.store import stamps
from machine.text import QUOTED_HISTORY_KEPT, encoded, open_copy, seal_copy, trim_quoted_history
from machine.timing import _REQUEST_TIMING
import meet_link
import message_seal
import pacing
import person_summary
import portable
import preparation_state
import recurring
import retention
import talk_live
import task_pages
import team_learnings
from timeutil import now
import voice_input
import whatsapp_images


class StoreCore:
    """The database: one per Machine. Store (assistant.py) adds the methods by table group."""

    exclusions = {}  # account id -> owner exclude rules, set by App from config

    owner_user_ids = set()  # The owner's own chat user IDs (Slack), set by App from config

    accounts = []  # configured accounts with their boundaries, set by App (Work/Personal labels)

    config = {}  # the service's config, set by App (browser and dashboard addresses for a card waiting on a sign-in)

    code_version = None  # the running code's version, set by watch_faults (error reports carry it)

    def __init__(self, path, protect=None):
        """`protect`: seal message contents (True), open them again (False), or keep what the database has (None).
        See message_seal.py."""
        self.path = Path(path).expanduser()
        self.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        key = message_seal.load_key(self.path)
        self.sealer = message_seal.Sealer(key) if key else None
        self.protected, self._sealed_schema = False, None
        with self.connect() as db:
            db.executescript('''
              PRAGMA journal_mode=WAL;
              CREATE TABLE IF NOT EXISTS facts(id INTEGER PRIMARY KEY,text TEXT NOT NULL,decision_id TEXT NOT NULL,suggestion_id TEXT,created_at TEXT NOT NULL,removed_at TEXT);
              CREATE TABLE IF NOT EXISTS push_subscriptions(endpoint TEXT PRIMARY KEY,p256dh TEXT NOT NULL,auth TEXT NOT NULL,created_at TEXT NOT NULL,last_status INTEGER,last_sent_at TEXT);
              CREATE TABLE IF NOT EXISTS android_inbox(id TEXT PRIMARY KEY,payload TEXT NOT NULL,received_at TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS android_receipts(id TEXT PRIMARY KEY,account_id TEXT NOT NULL,processed_at TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS android_feed_health(id INTEGER PRIMARY KEY,last_checked TEXT,last_recorded TEXT,error TEXT);
              CREATE TABLE IF NOT EXISTS events(
                id INTEGER PRIMARY KEY AUTOINCREMENT, account_id TEXT NOT NULL, source_id TEXT NOT NULL,
                kind TEXT NOT NULL, occurred_at TEXT NOT NULL, title TEXT NOT NULL,
                body TEXT NOT NULL, metadata TEXT NOT NULL, deleted INTEGER NOT NULL DEFAULT 0,
                content_hash TEXT NOT NULL, version INTEGER NOT NULL DEFAULT 1,
                analyzed_version INTEGER NOT NULL DEFAULT 0, ingested_at TEXT NOT NULL,
                UNIQUE(account_id,source_id));
              CREATE INDEX IF NOT EXISTS events_pending ON events(analyzed_version,version);
              CREATE INDEX IF NOT EXISTS events_account_time ON events(account_id,occurred_at);
              CREATE TABLE IF NOT EXISTS checkpoints(
                account_id TEXT PRIMARY KEY,state TEXT NOT NULL,last_success TEXT,error TEXT,
                error_at TEXT,failures INTEGER NOT NULL DEFAULT 0);
              CREATE TABLE IF NOT EXISTS sync_activity(
                id TEXT PRIMARY KEY,account_id TEXT NOT NULL,at TEXT NOT NULL,
                status TEXT NOT NULL,signals INTEGER,error TEXT,retry_at TEXT);
              CREATE INDEX IF NOT EXISTS sync_activity_account_time ON sync_activity(account_id,at);
              CREATE TABLE IF NOT EXISTS analyses(
                id TEXT PRIMARY KEY,started_at TEXT NOT NULL,finished_at TEXT,items TEXT NOT NULL,
                status TEXT NOT NULL,summary TEXT);
              CREATE TABLE IF NOT EXISTS suggestions(
                id TEXT PRIMARY KEY,dedupe_key TEXT UNIQUE NOT NULL,title TEXT NOT NULL,
                body TEXT NOT NULL,event_ids TEXT NOT NULL,account_ids TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',created_at TEXT NOT NULL,snoozed_until TEXT);
              CREATE TABLE IF NOT EXISTS decisions(
                id TEXT PRIMARY KEY,suggestion_id TEXT NOT NULL REFERENCES suggestions(id),
                choice TEXT NOT NULL,feedback TEXT NOT NULL,source TEXT NOT NULL,created_at TEXT NOT NULL,
                UNIQUE(source,id));
              CREATE TABLE IF NOT EXISTS decision_annotations(
                decision_id TEXT PRIMARY KEY REFERENCES decisions(id),status TEXT NOT NULL,
                reason TEXT NOT NULL,superseded_by TEXT);
              CREATE TABLE IF NOT EXISTS deliveries(
                suggestion_id TEXT PRIMARY KEY REFERENCES suggestions(id),status TEXT NOT NULL,
                message_id TEXT,error TEXT,updated_at TEXT NOT NULL,needs_edit INTEGER NOT NULL DEFAULT 0);
              CREATE TABLE IF NOT EXISTS preparations(
                suggestion_id TEXT PRIMARY KEY,decision_id TEXT NOT NULL,job_id TEXT UNIQUE NOT NULL,
                status TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,
                error TEXT,reason TEXT,retry_at TEXT,attempts INTEGER NOT NULL DEFAULT 0);
              CREATE TABLE IF NOT EXISTS recaps(
                week TEXT PRIMARY KEY,status TEXT NOT NULL,created_at TEXT NOT NULL,message_id TEXT,error TEXT);
              CREATE TABLE IF NOT EXISTS feedback_prompts(
                request_id TEXT PRIMARY KEY,suggestion_id TEXT NOT NULL,card_id TEXT NOT NULL,title TEXT NOT NULL,
                status TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,
                message_id TEXT,error TEXT,retry_at TEXT,attempted_at TEXT);
              CREATE TABLE IF NOT EXISTS action_jobs(
                id TEXT PRIMARY KEY,suggestion_id TEXT NOT NULL,revision TEXT NOT NULL,payload TEXT NOT NULL,
                status TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,
                approval_id TEXT NOT NULL,source TEXT NOT NULL,rfc_message_id TEXT NOT NULL,
                message_id TEXT,error TEXT,retry_at TEXT,UNIQUE(suggestion_id,revision));
              CREATE TABLE IF NOT EXISTS thread_snoozes(
                job_id TEXT PRIMARY KEY,account_id TEXT NOT NULL,thread_id TEXT NOT NULL,until TEXT NOT NULL,
                status TEXT NOT NULL,error TEXT,attempts INTEGER NOT NULL DEFAULT 0,retry_at TEXT,
                created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS draft_edits(
                id TEXT PRIMARY KEY,suggestion_id TEXT NOT NULL,old_revision TEXT NOT NULL,new_revision TEXT NOT NULL,
                kind TEXT NOT NULL,before_subject TEXT,before_body TEXT NOT NULL,after_subject TEXT,after_body TEXT NOT NULL,
                source TEXT NOT NULL,created_at TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS draft_saves(
                suggestion_id TEXT NOT NULL,revision TEXT NOT NULL,saved_at TEXT NOT NULL,PRIMARY KEY(suggestion_id,revision));
              CREATE TABLE IF NOT EXISTS suggestion_keys(
                dedupe_key TEXT PRIMARY KEY,suggestion_id TEXT NOT NULL,created_at TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS tool_approval_proposals(
                id TEXT PRIMARY KEY,title TEXT NOT NULL,detail TEXT NOT NULL,created_at TEXT NOT NULL);
              CREATE TABLE IF NOT EXISTS profile_runs(
                run_id TEXT PRIMARY KEY,status TEXT NOT NULL,started_at TEXT NOT NULL,updated_at TEXT NOT NULL,
                finished_at TEXT,attempts INTEGER NOT NULL DEFAULT 0,error TEXT,draft TEXT);
              CREATE TABLE IF NOT EXISTS review_runs(
                run_id TEXT PRIMARY KEY,status TEXT NOT NULL,started_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,finished_at TEXT,attempts INTEGER NOT NULL DEFAULT 0,error TEXT);
              CREATE VIRTUAL TABLE IF NOT EXISTS event_search USING fts5(title,body,content='events',content_rowid='id');
              CREATE TRIGGER IF NOT EXISTS search_insert AFTER INSERT ON events BEGIN
                INSERT INTO event_search(rowid,title,body) VALUES(new.id,new.title,new.body); END;
              CREATE TRIGGER IF NOT EXISTS search_update AFTER UPDATE OF title,body ON events BEGIN
                INSERT INTO event_search(event_search,rowid,title,body) VALUES('delete',old.id,old.title,old.body);
                INSERT INTO event_search(rowid,title,body) VALUES(new.id,new.title,new.body); END;
            ''')
            prompt_columns={r['name'] for r in db.execute('PRAGMA table_info(feedback_prompts)')}
            if 'attempted_at' not in prompt_columns:
                db.execute('ALTER TABLE feedback_prompts ADD COLUMN attempted_at TEXT')
            if 'kind' not in prompt_columns:
                db.execute("ALTER TABLE feedback_prompts ADD COLUMN kind TEXT NOT NULL DEFAULT 'change'")
            columns = {r['name'] for r in db.execute('PRAGMA table_info(suggestions)')}
            if 'next_action' not in columns:
                db.execute('ALTER TABLE suggestions ADD COLUMN next_action TEXT')
            if 'feedback_until' not in columns:
                db.execute('ALTER TABLE suggestions ADD COLUMN feedback_until TEXT')
                db.execute('ALTER TABLE suggestions ADD COLUMN feedback_request_id TEXT')
            if 'resume_status' not in columns:
                db.execute('ALTER TABLE suggestions ADD COLUMN resume_status TEXT')
            if 'completed_from' not in columns:
                db.execute('ALTER TABLE suggestions ADD COLUMN completed_from TEXT')
            if 'feedback_kind' not in columns:
                db.execute('ALTER TABLE suggestions ADD COLUMN feedback_kind TEXT')
            if 'urgent' not in columns:
                db.execute('ALTER TABLE suggestions ADD COLUMN urgent INTEGER NOT NULL DEFAULT 0')
            for column in ['deliver_after', 'source_line', 'due_at']:  # due_at: a due time, when the owner gave one (New to-do)
                if column not in columns:
                    db.execute('ALTER TABLE suggestions ADD COLUMN '+column+' TEXT')
            for column in ['feedback_requested_at','feedback_after_message_id','feedback_prompt_message_id','feedback_card_message_id']:
                if column not in columns:
                    db.execute('ALTER TABLE suggestions ADD COLUMN '+column+' TEXT')
            for column in ['closed_from','closed_decision_id','undo_until','closed_state']:
                if column not in columns:
                    db.execute('ALTER TABLE suggestions ADD COLUMN '+column+' TEXT')
            # A to-do whose whole point is a moment (a confirmation or reminder before a meeting): the review's expires_at and
            # expires_what ("the meeting with Sam"). Once it passes the to-do closes by itself (Store.expire_passed: expired_at).
            for column in ['expires_at','expires_what','expired_at']:
                if column not in columns:
                    db.execute('ALTER TABLE suggestions ADD COLUMN '+column+' TEXT')
            # The message from someone else the to-do's draft or decision follows (a teammate's input in Slack, another
            # thread): the review's or the preparation's based_on (Store.mark_based_on). The to-do shows it ("Based on Sam in #ops").
            if 'based_on' not in columns:
                db.execute('ALTER TABLE suggestions ADD COLUMN based_on INTEGER')
            # A to-do its confirmed final step closed by itself, in a run the owner didn't watch (a submitted form, a filed
            # issue): when, until the owner saw it. The list shows it under Just done and the phone hears of it (report_done).
            if 'done_report' not in columns:
                db.execute('ALTER TABLE suggestions ADD COLUMN done_report TEXT')
            delivery_columns = {r['name'] for r in db.execute('PRAGMA table_info(deliveries)')}
            if 'reminder' not in delivery_columns:
                db.execute('ALTER TABLE deliveries ADD COLUMN reminder INTEGER NOT NULL DEFAULT 0')
                db.execute("ALTER TABLE deliveries ADD COLUMN previous_message_ids TEXT NOT NULL DEFAULT '[]'")
                db.execute('ALTER TABLE deliveries ADD COLUMN last_notified_at TEXT')
                db.execute("UPDATE deliveries SET last_notified_at=updated_at WHERE status='sent'")
            if 'edit_failures' not in delivery_columns:
                db.execute('ALTER TABLE deliveries ADD COLUMN edit_failures INTEGER NOT NULL DEFAULT 0')
                db.execute('ALTER TABLE deliveries ADD COLUMN edit_retry_at TEXT')
            if 'notification_message_id' not in delivery_columns:
                db.execute('ALTER TABLE deliveries ADD COLUMN notification_message_id TEXT')
            if 'send_kind' not in delivery_columns:
                db.execute("ALTER TABLE deliveries ADD COLUMN send_kind TEXT NOT NULL DEFAULT 'card'")
            checkpoint_columns = {r['name'] for r in db.execute('PRAGMA table_info(checkpoints)')}
            if 'last_sync_signals' not in checkpoint_columns:
                db.execute('ALTER TABLE checkpoints ADD COLUMN last_sync_signals INTEGER')
            if 'retry_at' not in checkpoint_columns:
                db.execute('ALTER TABLE checkpoints ADD COLUMN retry_at TEXT')
            review_columns = {r['name'] for r in db.execute('PRAGMA table_info(analyses)')}
            for column in ['owner_session', 'owner_run', 'last_error', 'error_at', 'resumed_at', 'resumed_from']:
                if column not in review_columns:
                    db.execute('ALTER TABLE analyses ADD COLUMN ' + column + ' TEXT')
            if 'attempts' not in review_columns:
                db.execute('ALTER TABLE analyses ADD COLUMN attempts INTEGER NOT NULL DEFAULT 1')
            if 'room' not in {r['name'] for r in db.execute('PRAGMA table_info(profile_runs)')}:
                db.execute('ALTER TABLE profile_runs ADD COLUMN room INTEGER')
            if 'evidence' not in {r['name'] for r in db.execute('PRAGMA table_info(profile_runs)')}:
                db.execute('ALTER TABLE profile_runs ADD COLUMN evidence TEXT')
            if 'kind' not in {r['name'] for r in db.execute('PRAGMA table_info(profile_runs)')}:
                db.execute("ALTER TABLE profile_runs ADD COLUMN kind TEXT NOT NULL DEFAULT 'profile'")
            if 'auto' not in {r['name'] for r in db.execute('PRAGMA table_info(profile_runs)')}:
                db.execute('ALTER TABLE profile_runs ADD COLUMN auto INTEGER NOT NULL DEFAULT 0')
            worker_columns = {r['name'] for r in db.execute('PRAGMA table_info(review_runs)')}
            for column in ['retry_at', 'unavailable_since', 'error_phase', 'last_error', 'last_error_phase', 'error_at']:
                if column not in worker_columns:
                    db.execute('ALTER TABLE review_runs ADD COLUMN ' + column + ' TEXT')
            if 'preview' not in worker_columns:
                db.execute('ALTER TABLE review_runs ADD COLUMN preview INTEGER NOT NULL DEFAULT 0')
            if 'auto' not in worker_columns:  # a preview The Machine started by itself: the first look
                db.execute('ALTER TABLE review_runs ADD COLUMN auto INTEGER NOT NULL DEFAULT 0')
            if 'planned' not in worker_columns:  # how many signals the run set out to review, for its progress
                db.execute('ALTER TABLE review_runs ADD COLUMN planned INTEGER')
            if 'window_hours' not in worker_columns:  # a quick first look: only this many hours back, at most `budget` signals
                db.execute('ALTER TABLE review_runs ADD COLUMN window_hours INTEGER')
                db.execute('ALTER TABLE review_runs ADD COLUMN budget INTEGER')
            if 'promising' not in worker_columns:  # the review after the quick look: the most promising signals first
                db.execute('ALTER TABLE review_runs ADD COLUMN promising INTEGER NOT NULL DEFAULT 0')
            # When setup steps first happened (first import per source, first card shown): timestamps and counts only.
            # `tracking_since` tells a new install from one that had cards before this was recorded.
            db.execute('CREATE TABLE IF NOT EXISTS milestones(name TEXT PRIMARY KEY,at TEXT NOT NULL,detail TEXT)')
            # The Calendar form's own writes, one row per owner tap (request_id): a repeated tap is that same write. payload is
            # a hash of the change and result the Google event id, so no event text is kept here.
            db.execute('CREATE TABLE IF NOT EXISTS calendar_writes(id TEXT PRIMARY KEY,account_id TEXT NOT NULL,op TEXT NOT NULL,payload TEXT NOT NULL,'
                       'status TEXT NOT NULL,result TEXT,error TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL)')
            # First-look cards its reviewer wanted prepared ahead, prepared once reviews are on (Store.prepare_first_look)
            db.execute('CREATE TABLE IF NOT EXISTS first_look_ahead(suggestion_id TEXT PRIMARY KEY,created_at TEXT NOT NULL)')
            db.execute("INSERT OR IGNORE INTO milestones(name,at) VALUES('tracking_since',?)", (now(),))
            if 'due' not in columns:
                db.execute('ALTER TABLE suggestions ADD COLUMN due TEXT')
            if 'handled_hint' not in columns:
                db.execute('ALTER TABLE suggestions ADD COLUMN handled_hint TEXT')
            if 'early' not in columns:
                db.execute('ALTER TABLE suggestions ADD COLUMN early INTEGER NOT NULL DEFAULT 0')
            if 'awaiting' not in columns:
                db.execute('ALTER TABLE suggestions ADD COLUMN awaiting TEXT')
            if 'outcome' not in columns:
                db.execute('ALTER TABLE suggestions ADD COLUMN outcome TEXT')
            # A card the owner made themselves: origin 'owner' (NULL is The Machine's own) and what they typed, kept as is.
            # title_suggested: the generated title, held while the owner's own title is in `title` (a rename); NULL when
            # not renamed. Every reader of `title` (Telegram, push, the Fleet, the CLI, older dashboards) shows theirs.
            # merge_offer: on an owner's card, the card the review thinks it is the same as ({"card_id"}, "kept" once they said no).
            for column in ['origin', 'owner_words', 'title_suggested', 'merge_offer']:
                if column not in columns:
                    db.execute('ALTER TABLE suggestions ADD COLUMN ' + column + ' TEXT')
            if 'title_source' not in columns:  # 'auto': written by The Machine and kept current; 'user': the owner named it
                db.execute("ALTER TABLE suggestions ADD COLUMN title_source TEXT NOT NULL DEFAULT 'auto'")
            if 'kind' not in {r['name'] for r in db.execute('PRAGMA table_info(facts)')}:
                db.execute("ALTER TABLE facts ADD COLUMN kind TEXT NOT NULL DEFAULT 'fact'")
            if 'merged_into' not in {r[1] for r in db.execute('PRAGMA table_info(facts)')}:  # condensed: 'fact:<id>' or 'voice:<channel>'
                db.execute('ALTER TABLE facts ADD COLUMN merged_into TEXT')
            # What sort of fact (FACT_SORTS: event, commitment, preference or fact; NULL on a draft rule and on older ones,
            # read as fact), the day it stops holding (valid_until, YYYY-MM-DD, through that day) and when it was last said
            # again (confirmed_at: its decay starts over). Past valid_until the condense pass retires it as 'expired:<id>'.
            have_facts = {r[1] for r in db.execute('PRAGMA table_info(facts)')}
            # source: who told it when it wasn't the owner's own note ('ai:<name>': a connected AI, ai_app.py); NULL: the owner.
            # side: a connected AI's fact is in that AI's area (work or personal), so it stays out of the other one's preparations
            for column in ('fact_kind', 'valid_until', 'confirmed_at', 'source', 'side'):
                if column not in have_facts:
                    db.execute('ALTER TABLE facts ADD COLUMN ' + column + ' TEXT')
            # Who a fact is about: a person, organization or project in the graph (its node id), never the owner, who is no node.
            # A fact without one is about the owner or the world and shows on nobody's page. removed_at: the owner said it isn't about them.
            db.execute('CREATE TABLE IF NOT EXISTS fact_about(fact_id INTEGER NOT NULL,node_id TEXT NOT NULL,by TEXT NOT NULL,created_at TEXT NOT NULL,removed_at TEXT,PRIMARY KEY(fact_id,node_id))')
            # What each Change note was: a style fix, a missing fact, keep going, or a new ask.
            db.execute('CREATE TABLE IF NOT EXISTS note_kinds(decision_id TEXT PRIMARY KEY,suggestion_id TEXT NOT NULL,kind TEXT NOT NULL,source TEXT NOT NULL,created_at TEXT NOT NULL)')
            # Changes to how cards and drafts are made, shown on the hit-rate chart.
            db.execute('CREATE TABLE IF NOT EXISTS rule_changes(id INTEGER PRIMARY KEY,at TEXT NOT NULL,kind TEXT NOT NULL,text TEXT NOT NULL,ref TEXT)')
            # The weekly recap as sent (its text, so a tap's result shows in place) and the lines it offers a choice on:
            # a busy source to filter or keep, a card snoozed again and again to drop, do now or keep.
            if 'text' not in {r[1] for r in db.execute('PRAGMA table_info(recaps)')}:
                db.execute('ALTER TABLE recaps ADD COLUMN text TEXT')
            db.execute('CREATE TABLE IF NOT EXISTS recap_items(id TEXT PRIMARY KEY,week TEXT NOT NULL,n INTEGER NOT NULL,kind TEXT NOT NULL,ref TEXT,'
                       'line TEXT NOT NULL,data TEXT NOT NULL,status TEXT NOT NULL,decision_id TEXT,decided_at TEXT)')
            # Each choice goes out as its own message (with its own buttons), so a tap is checked against that one.
            if 'message_id' not in {r[1] for r in db.execute('PRAGMA table_info(recap_items)')}:
                db.execute('ALTER TABLE recap_items ADD COLUMN message_id TEXT')
            # How the owner writes, a short block per channel (and All): learned from their style notes, their edits
            # and their own messages, editable in Settings. Like facts, what was learned, not what messages say.
            db.execute('CREATE TABLE IF NOT EXISTS voices(channel TEXT PRIMARY KEY,text TEXT NOT NULL,source TEXT NOT NULL,ref TEXT,updated_at TEXT NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS voice_merges(channel TEXT PRIMARY KEY,previous TEXT,merged_text TEXT NOT NULL,merged_ref TEXT)')
            # Notes about one kind of task, offered as a skill on a card (Create skill / Update <skill> / Not now).
            # fact_ids: the notes; target_id: the owner's own skill they'd go into, else a new one with name/description/body.
            db.execute('CREATE TABLE IF NOT EXISTS skill_clusters(id TEXT PRIMARY KEY,fact_ids TEXT NOT NULL,name TEXT NOT NULL,description TEXT NOT NULL,'
                       'body TEXT NOT NULL,target_id TEXT,target_name TEXT,suggestion_id TEXT,status TEXT NOT NULL,skill_id TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL)')
            # Checked against the owner's skills first (checked=1): related_* names a separate skill it sits next to, with
            # relation in one line; base_sha is the target skill the update's body (the whole skill, rewritten) was written on,
            # reviewed_sha the target as the owner saw it in the before/after on Update. No base_sha: an older addition.
            have = {r[1] for r in db.execute('PRAGMA table_info(skill_clusters)')}
            for column in ('related_id TEXT', 'related_name TEXT', 'relation TEXT', 'checked INTEGER', 'reviewed_sha TEXT', 'base_sha TEXT'):
                if column.split()[0] not in have:
                    db.execute('ALTER TABLE skill_clusters ADD COLUMN ' + column)
            # What a fact means, to pick the ones a task needs (when embeddings are on).
            db.execute('CREATE TABLE IF NOT EXISTS fact_vectors(fact_id INTEGER PRIMARY KEY,model TEXT NOT NULL,vector BLOB NOT NULL)')
            # Offered to one review once: an edit (or the owner's own reply instead of the draft) by its id,
            # an unlearned style note as 'note:<decision id>', and the condense pass as 'condense:<date>'.
            db.execute('CREATE TABLE IF NOT EXISTS edits_offered(edit_id TEXT PRIMARY KEY,run_id TEXT NOT NULL,offered_at TEXT NOT NULL)')
            # Emails offered to a review as possibly slipped, so each is offered once.
            db.execute('CREATE TABLE IF NOT EXISTS slipped(event_id INTEGER PRIMARY KEY,kind TEXT NOT NULL,run_id TEXT,offered_at TEXT NOT NULL)')
            # The service's own errors per code location and day: where, and the latest message with anything
            # private taken out (fault_message), never values or content.
            db.execute('CREATE TABLE IF NOT EXISTS faults(fingerprint TEXT NOT NULL,day TEXT NOT NULL,kind TEXT NOT NULL,frames TEXT NOT NULL,'
                       'location TEXT NOT NULL,version TEXT,first_at TEXT NOT NULL,last_at TEXT NOT NULL,count INTEGER NOT NULL,'
                       'reported INTEGER NOT NULL DEFAULT 0,PRIMARY KEY(fingerprint,day))')
            fault_columns = {r['name'] for r in db.execute('PRAGMA table_info(faults)')}
            if 'message' not in fault_columns:
                db.execute('ALTER TABLE faults ADD COLUMN message TEXT')
            if 'origin' not in fault_columns:  # an outside service that failed (fault_origin), as JSON
                db.execute('ALTER TABLE faults ADD COLUMN origin TEXT')
            # Keep version timing independently of daily signal aggregation. Legacy rows only
            # prove their last occurrence belongs to their last recorded version.
            db.execute('CREATE TABLE IF NOT EXISTS fault_versions(fingerprint TEXT NOT NULL,version TEXT NOT NULL,day TEXT NOT NULL,kind TEXT NOT NULL,'
                       'first_at TEXT NOT NULL,last_at TEXT NOT NULL,count INTEGER NOT NULL,PRIMARY KEY(fingerprint,version,day))')
            db.execute('INSERT OR IGNORE INTO fault_versions SELECT fingerprint,version,day,kind,last_at,last_at,1 FROM faults WHERE version IS NOT NULL')
            # Git receipts survive a service restart before optional push/restart work.
            db.execute('CREATE TABLE IF NOT EXISTS merge_effects(action_id TEXT NOT NULL,operation TEXT NOT NULL,receipt TEXT NOT NULL,status TEXT NOT NULL,'
                       'updated_at TEXT NOT NULL,PRIMARY KEY(action_id,operation))')
            db.execute(task_pages.SCHEMA)  # task pages offered or shared from handoffs by email (task_pages.py)
            db.execute(meet_link.SCHEMA)  # booking links for meetings with someone without a Machine (meet_link.py), sealed at rest
            handoff_mail.ensure(db)  # handoffs by email and their take links (handoff_mail.py)
            team_learnings.ensure(db)  # learnings for The Machine team (team_learnings.py), with their use cases
            error_feed.ensure(db)  # error reports for The Machine team: signatures only (error_feed.py)
            activity.ensure(db)  # daily activity counts for the hosted health report (activity.py)
            activity_log.ensure(db)  # Activity: the connections it has seen, for added and removed lines (activity_log.py)
            ai_access.ensure(db)  # connected AIs: their connections, sign-ins and activity (ai_access.py)
            pacing.ensure(db)  # how often background work paced (pacing.py): made here, not inside someone's write
            learning_loop.ensure(db)  # the learning loop's changes, each undoable (learning_loop.py)
            person_summary.ensure(db)  # the summary on top of a person's page (person_summary.py)
            # Promises the owner made and promises made to them, from reviewed messages. Each is
            # checked when due: still open, it becomes a card (status carded, suggestion_id).
            db.execute('CREATE TABLE IF NOT EXISTS promises(id INTEGER PRIMARY KEY,direction TEXT NOT NULL,who TEXT NOT NULL,what TEXT NOT NULL,due TEXT,'
                       'check_at TEXT NOT NULL,event_id INTEGER NOT NULL,account_id TEXT NOT NULL,watch TEXT,status TEXT NOT NULL,note TEXT,suggestion_id TEXT,'
                       'created_at TEXT NOT NULL,updated_at TEXT NOT NULL,UNIQUE(event_id,direction,who,what))')
            promise_sql = db.execute("SELECT sql FROM sqlite_master WHERE name='promises'").fetchone()[0]
            if re.search(r'UNIQUE\s*\(event_id,\s*direction,\s*who\)', promise_sql, re.I):
                if not db.in_transaction:
                    db.execute('BEGIN IMMEDIATE')
                db.execute(re.sub(r'UNIQUE\s*\(event_id,\s*direction,\s*who\)', 'UNIQUE(event_id,direction,who,what)', re.sub(r'^CREATE TABLE\s+"?promises"?', 'CREATE TABLE promises_next', promise_sql, count=1), flags=re.I))
                db.execute('INSERT INTO promises_next SELECT * FROM promises')
                db.execute('DROP TABLE promises')
                db.execute('ALTER TABLE promises_next RENAME TO promises')
            db.execute("CREATE INDEX IF NOT EXISTS promises_open ON promises(status,check_at)")
            # What happened to a promise after it was recorded, for its page: a kind and a date or id, never message text
            db.execute('CREATE TABLE IF NOT EXISTS promise_log(id INTEGER PRIMARY KEY,promise_id INTEGER NOT NULL,at TEXT NOT NULL,kind TEXT NOT NULL,detail TEXT)')
            db.execute('CREATE INDEX IF NOT EXISTS promise_log_promise ON promise_log(promise_id)')
            if 'together' not in {r['name'] for r in db.execute('PRAGMA table_info(promises)')}:
                db.execute('ALTER TABLE promises ADD COLUMN together INTEGER NOT NULL DEFAULT 0')  # a plan made with them: theirs and the owner's
            if 'owner_step' not in {r['name'] for r in db.execute('PRAGMA table_info(promises)')}:
                db.execute('ALTER TABLE promises ADD COLUMN owner_step INTEGER NOT NULL DEFAULT 0')  # only the owner can do it (go there, pick it up)
            preparation_columns = {r['name'] for r in db.execute('PRAGMA table_info(preparations)')}
            if 'action_id' not in preparation_columns:
                db.execute('ALTER TABLE preparations ADD COLUMN action_id TEXT')
                db.execute("UPDATE preparations SET action_id=(SELECT id FROM action_jobs WHERE approval_id=preparations.decision_id AND suggestion_id=preparations.suggestion_id AND status='local_preparation')")
            # move_to: the area a stuck run asks to be moved to; use_events: messages from another area it asks to use (JSON ids)
            for column in ['details', 'started_at', 'questions', 'move_to', 'use_events']:
                if column not in preparation_columns:
                    db.execute('ALTER TABLE preparations ADD COLUMN ' + column + ' TEXT')
            if 'auto_retries' not in preparation_columns:
                db.execute('ALTER TABLE preparations ADD COLUMN auto_retries INTEGER NOT NULL DEFAULT 0')
            if 'deferrals' not in {r['name'] for r in db.execute('PRAGMA table_info(events)')}:
                db.execute('ALTER TABLE events ADD COLUMN deferrals INTEGER NOT NULL DEFAULT 0')
                # Count earlier deferrals of each event's current version.
                db.execute('''UPDATE events SET deferrals=(SELECT count(*) FROM analyses a, json_each(a.items) j
                    WHERE a.status='complete' AND json_extract(j.value,'$.deferred')=1
                      AND json_extract(j.value,'$.id')=events.id AND json_extract(j.value,'$.version')=events.version)
                    WHERE analyzed_version<version''')
        with self.connect() as db:
            preparation_state.initialize(db)
            retention.initialize(db)
            chat_files.initialize(db)
            whatsapp_images.ensure(db)
            chat_model.initialize(db)
            voice_input.initialize(db)
            talk_live.initialize(db)
            db.execute('CREATE TABLE IF NOT EXISTS chat_stops(job_id TEXT PRIMARY KEY,suggestion_id TEXT NOT NULL,text TEXT NOT NULL,at TEXT NOT NULL)')
            if 'via' not in {r['name'] for r in db.execute('PRAGMA table_info(chat_stops)')}:  # where Stop was pressed: NULL the chat, 'browser'
                db.execute('ALTER TABLE chat_stops ADD COLUMN via TEXT')
        os.chmod(self.path, 0o600)
        self.ensure_monotonic_event_ids()
        with self.connect() as db:
            # Backlog counts/selection filter on a column comparison that the plain
            # events_pending index cannot serve; this keeps them off a full scan.
            db.execute('CREATE INDEX IF NOT EXISTS events_pending_account ON events(account_id,ingested_at,id) WHERE analyzed_version<version')
            history_store.ensure(db)  # after the monotonic-ID rebuild, as its indexes are
            # A thread's messages by its key: a person's page asks which of its threads are automated mail (shared_graph
            # Scope.automated_only), and bounces and replies look up a thread's messages, without a pass over all mail
            db.execute("CREATE INDEX IF NOT EXISTS events_thread_id ON events(json_extract(metadata,'$.thread_id'))")
            db.execute("CREATE INDEX IF NOT EXISTS events_conversation ON events(json_extract(metadata,'$.conversation_id'))")
            # The few kinds a record's timeline reads in full on each page open (graph.timeline: the owner's to-dos, Zoom
            # summaries, Intercom conversations, notes and transcripts added to meetings), each a pass over all events
            # without these. One partial index per kind, never one on kind itself: SQLite would then pick it over the
            # better index of many other queries.
            for sql in ("CREATE INDEX IF NOT EXISTS events_kind_owner_card ON events(occurred_at) WHERE kind='owner.card'",
                        "CREATE INDEX IF NOT EXISTS events_kind_zoom_summary ON events(occurred_at) WHERE kind='zoom.summary'",
                        "CREATE INDEX IF NOT EXISTS events_kind_intercom_conversation ON events(occurred_at) WHERE kind='intercom.conversation'",
                        "CREATE INDEX IF NOT EXISTS events_kind_meeting_notes ON events(occurred_at) WHERE kind='meeting.notes'",
                        "CREATE INDEX IF NOT EXISTS events_kind_meeting_transcript ON events(occurred_at) WHERE kind='meeting.transcript'"):
                db.execute(sql)
            db.execute('CREATE INDEX IF NOT EXISTS analyses_owner ON analyses(owner_run,owner_session)')
            # A to-do's decisions: the to-do list and the Done list ask each to-do's latest one, a pass over all decisions each
            db.execute('CREATE INDEX IF NOT EXISTS decisions_suggestion ON decisions(suggestion_id,created_at)')
            for schema in embeddings.SCHEMAS:  # after the monotonic-ID migration, which rebuilds events
                db.execute(schema)
            graph.ensure(db)
            follow_ups.ensure(db)  # automated follow-ups on boards and projects (follow_ups.py): new tables only
            bounces.ensure(db)  # addresses that bounce (bounces.py): new tables only
            # Change counters for what a status poll keeps between requests, after the tables (machine/store/stamps.py: graph.waiting, graph.slack_names)
            stamps.watch(db, ('graph_nodes', 'person_roles', 'identity_names', 'slack_members'))
            recurring.ensure(db)  # recurring to-dos (recurring.py): new tables only
            if 'project' not in {r[1] for r in db.execute('PRAGMA table_info(suggestions)')}:
                db.execute('ALTER TABLE suggestions ADD COLUMN project TEXT')
            # Who set a to-do's project: 'review' (or NULL, from before 2026-10-27), 'auto' (graph.link_cards: its thread or
            # people are on it) or 'owner' (by hand, also "no project"), which nothing automatic changes again.
            # A to-do the owner moved to another area (todo_areas.py): that area, so a later signal from the old one doesn't
            # pull it back; card_moves keeps what each move changed, for its event line and Undo.
            if 'area' not in {r[1] for r in db.execute('PRAGMA table_info(suggestions)')}:
                db.execute('ALTER TABLE suggestions ADD COLUMN area TEXT')
            db.execute('CREATE TABLE IF NOT EXISTS card_moves(decision_id TEXT PRIMARY KEY,suggestion_id TEXT NOT NULL,area TEXT NOT NULL,'
                       'accounts_before TEXT NOT NULL,area_before TEXT,created_at TEXT NOT NULL,undone_at TEXT)')
            # Messages from another area the owner let a stuck run use (Store.use_sources): its event line
            db.execute('CREATE TABLE IF NOT EXISTS card_uses(decision_id TEXT PRIMARY KEY,suggestion_id TEXT NOT NULL,event_ids TEXT NOT NULL,'
                       'mail INTEGER NOT NULL,created_at TEXT NOT NULL)')
            if 'project_by' not in {r[1] for r in db.execute('PRAGMA table_info(suggestions)')}:
                db.execute('ALTER TABLE suggestions ADD COLUMN project_by TEXT')
                db.execute("UPDATE suggestions SET project_by='review' WHERE project IS NOT NULL AND project<>''")
            # A step only the owner can do themselves, in person or offline (a visit, a pickup, attending): the review's
            # judgment. The card offers Mark done and help around it (Plan it), never Do it.
            if 'owner_step' not in {r[1] for r in db.execute('PRAGMA table_info(suggestions)')}:
                db.execute('ALTER TABLE suggestions ADD COLUMN owner_step INTEGER NOT NULL DEFAULT 0')
            # Notes saved before a meeting's Notes and Transcript were apart: a transcript among them becomes the meeting's
            # Transcript, once (what each row was is kept in meeting_moves)
            moved = self.move_meeting_transcripts(db)
            if moved:
                LOG.info('Moved %d meeting transcript(s) out of Notes into Transcript: %s', len(moved), moved)
        restored = self.restore_ahead_blockers()
        if restored:
            LOG.info('Showed the blocker again on %d prepared-ahead to-do(s)', restored)
        self.clean_protection_leftovers()
        try:
            self.message_protection(True if protect is None and os.environ.get('MESSAGE_PROTECTION_TEST') else protect)
        except Exception as error:  # the app keeps running as it was; the next start tries again
            with self.connect() as db:
                sealed = message_seal.is_protected(db)
            if sealed and not self.sealer:
                raise
            self.protected = sealed
            LOG.error('Message protection left as it was (%s): %s', 'sealed' if sealed else 'plain', error)

    def message_protection(self, protect):
        """Bring the database to the wanted state: sealed message contents, or plain. A change is one transaction,
        after a consistent copy of the database, encrypted with the message key in a private folder (put back when the
        change does not check out, overwritten and removed once it does), then a VACUUM so no page keeps the old text.
        Returns what changed, or None."""
        with self.connect() as db:
            sealed = message_seal.is_protected(db)
            if sealed and not self.sealer:
                raise message_seal.SealError(f'The messages in {self.path} are sealed and {message_seal.key_path(self.path)} is missing')
            if sealed and protect is not False:
                self.protected = True
                return None
            if not sealed and not protect:
                return None
        if not self.sealer:
            self.sealer = message_seal.Sealer(message_seal.load_key(self.path, create=True))
        safety = self.safety_dir()
        safety.mkdir(mode=0o700, exist_ok=True)
        os.chmod(safety, 0o700)
        copy = safety / (self.path.name + '.before-protection.sealed')
        portable.shred(copy)
        seal_copy(self.path, copy, message_seal.load_key(self.path))
        changed, restored, done = None, False, False
        try:
            with self.connect() as db:
                db.execute('BEGIN IMMEDIATE')
                changed = message_seal.protect(db) if protect else message_seal.unprotect(db) or {}
                if protect and message_seal.leftovers(db):
                    raise message_seal.SealError('Some message contents could not be sealed; nothing was changed')
            self.protected = bool(protect)
            try:
                self.check_sealed()  # every sealed value opens with this key before the copy goes
            except Exception:
                restored = self.restore_copy(copy)
                raise
            with contextlib.closing(sqlite3.connect(self.path, timeout=60)) as db:
                db.execute('PRAGMA secure_delete=ON')
                db.execute('VACUUM')
                db.execute('PRAGMA wal_checkpoint(TRUNCATE)')
            done = True
        finally:
            if done or changed is None or restored or self.database_ok():
                portable.shred_tree(safety)  # unchanged, put back, or checked: the copy is not needed
            else:
                LOG.error('The encrypted copy of the database before the change is kept at %s', copy)
        LOG.info('message contents %s: %s', 'sealed' if protect else 'opened', changed)
        return changed

    def safety_dir(self):
        """The private folder (700) next to the database that holds its encrypted copy while message protection
        switches on or off."""
        return self.path.with_name('.' + self.path.name + '.before-protection.d')

    def check_sealed(self):
        with self.connect() as db:
            for table, column, _ in message_seal.sealed_columns(db):
                for _ in db.execute(f'SELECT {column} FROM {table}'):
                    pass

    def database_ok(self):
        """The live database is whole and, when sealed, every sealed value opens with this Machine's key."""
        try:
            with contextlib.closing(sqlite3.connect(self.path, timeout=60)) as db:
                if db.execute('PRAGMA quick_check').fetchone()[0] != 'ok':
                    return False
                sealed = message_seal.is_protected(db)
            if sealed and not self.sealer:
                return False
            if sealed or self.sealer:
                self.check_sealed()
            return True
        except Exception as error:
            LOG.error('The database did not check out: %s', error)
            return False

    def restore_copy(self, copy):
        """Put the encrypted copy back over the live database. The plain copy only exists in the private folder
        for the moment it takes, and is overwritten before it is removed."""
        plain = copy.with_name(copy.name.replace('.sealed', '.tmp'))
        try:
            open_copy(copy, plain, message_seal.load_key(self.path))
            with contextlib.closing(sqlite3.connect(plain)) as source, contextlib.closing(sqlite3.connect(self.path, timeout=60)) as target:
                source.backup(target)
            with contextlib.closing(sqlite3.connect(self.path)) as db:
                self.protected = bool(message_seal.is_protected(db))
            LOG.error('Message protection did not check out; the database was put back as it was')
            return True
        except Exception as error:
            LOG.error('The database could not be put back from %s: %s', copy, error)
            return False
        finally:
            portable.shred(plain)

    def clean_protection_leftovers(self):
        """Copies an interrupted switch left behind: a plain events.sqlite.before-protection from earlier versions,
        and the private folder with its encrypted copy. Removed (overwritten first) once the live database checks
        out; an encrypted copy is put back when it does not. What can't be cleaned, doctor reports."""
        legacy = self.path.with_name(self.path.name + '.before-protection')
        safety = self.safety_dir()
        if not legacy.exists() and not safety.exists():
            return
        if not self.database_ok():
            copy = safety / (self.path.name + '.before-protection.sealed')
            if not (copy.is_file() and self.restore_copy(copy) and self.database_ok()):
                LOG.error('Left the copies from an interrupted message protection change in place: the database did not check out')
                return
        portable.shred(legacy)
        portable.shred_tree(safety)
        LOG.info('Removed the copies an interrupted message protection change left behind')

    def ensure_monotonic_event_ids(self):
        # Purged evidence IDs remain in review/suggestion provenance. Never let
        # SQLite reuse an old ID for an unrelated later message.
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            schema = db.execute("SELECT sql FROM sqlite_master WHERE name='events'").fetchone()[0]
            if 'AUTOINCREMENT' not in schema.upper():
                migration = re.sub(r'^CREATE TABLE\s+"?events"?', 'CREATE TABLE events_monotonic', schema, count=1)
                db.execute(migration.replace('id INTEGER PRIMARY KEY,', 'id INTEGER PRIMARY KEY AUTOINCREMENT,', 1))
                db.execute('INSERT INTO events_monotonic SELECT * FROM events')
                db.execute('DROP TABLE events')
                db.execute('ALTER TABLE events_monotonic RENAME TO events')
                db.execute('CREATE INDEX events_pending ON events(analyzed_version,version)')
                db.execute('CREATE INDEX events_account_time ON events(account_id,occurred_at)')
                db.execute('''CREATE TRIGGER search_insert AFTER INSERT ON events BEGIN
                    INSERT INTO event_search(rowid,title,body) VALUES(new.id,new.title,new.body); END''')
                db.execute('''CREATE TRIGGER search_update AFTER UPDATE OF title,body ON events BEGIN
                    INSERT INTO event_search(event_search,rowid,title,body) VALUES('delete',old.id,old.title,old.body);
                    INSERT INTO event_search(rowid,title,body) VALUES(new.id,new.title,new.body); END''')
            db.execute('''CREATE TRIGGER IF NOT EXISTS search_delete AFTER DELETE ON events BEGIN
                INSERT INTO event_search(event_search,rowid,title,body) VALUES('delete',old.id,old.title,old.body); END''')

    def purge_excluded(self, account, rules):
        """Remove already-stored signals matching the owner's exclude rules; checkpoints untouched."""
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            rules = routine_rules(rules)[0]
            ids = [r['source_id'] for r in db.execute('SELECT source_id,title,body,metadata FROM events WHERE account_id=?', (account,))
                   if excluded_by_rules(rules, {'title': r['title'], 'body': r['body'], 'metadata': json.loads(r['metadata'])})]
            return self.exclude_sources(db, account, ids, reason='owner_exclude_rule')

    def exclude_sources(self, db, account, source_ids, reason='account_content_filter'):
        removed = set()
        for source_id in set(source_ids):
            row = db.execute('SELECT id FROM events WHERE account_id=? AND source_id=?',
                             (account, source_id)).fetchone()
            if row:
                removed.add(row['id'])
                db.execute('DELETE FROM events WHERE id=?', (row['id'],))
        if removed:
            # Keep historical review receipts, but clearly mark evidence that
            # the owner excluded. No source text is retained in these receipts.
            for review in db.execute('SELECT id,items FROM analyses').fetchall():
                items = json.loads(review['items'])
                if any(item['id'] in removed for item in items):
                    for item in items:
                        if item['id'] in removed:
                            item['excluded'] = reason
                    db.execute('UPDATE analyses SET items=? WHERE id=?', (encoded(items), review['id']))
        return len(removed)

    def trim_stored_quoted_history(self):
        """One-off cleanup: trim quoted reply history from already stored emails, as new
        mail is trimmed on collection. Run with the collector stopped. Versions and review
        state are unchanged; set-aside emails whose text changed are offered again."""
        changed = 0
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            rows = db.execute("SELECT * FROM events WHERE kind IN ('gmail.message','salesflare.email')").fetchall()
            for row in rows:
                metadata = json.loads(row['metadata'])
                if 'quoted_history_chars' in metadata:
                    continue
                if row['kind'] == 'salesflare.email':
                    header, _, text = row['body'].partition('\n\n')
                    text, quoted = trim_quoted_history(text, row['title'])
                    body = header + '\n\n' + text
                else:
                    body, quoted = trim_quoted_history(row['body'], row['title'])
                if not quoted:
                    continue
                # A body cut at the size limit was cut inside the quoted part.
                metadata.update(truncated=bool(metadata.get('truncated')) and len(body) > 40000,
                                quoted_history_chars=quoted, quoted_history_shortened=quoted > QUOTED_HISTORY_KEPT)
                event = {'account_id': row['account_id'], 'source_id': row['source_id'], 'kind': row['kind'],
                         'occurred_at': row['occurred_at'], 'title': row['title'], 'body': body,
                         'metadata': metadata, 'deleted': bool(row['deleted'])}
                db.execute('UPDATE events SET body=?,metadata=?,content_hash=?,deferrals=0 WHERE id=?',
                           (body, encoded(metadata), hashlib.sha256(encoded(event).encode()).hexdigest(), row['id']))
                changed += 1
        return {'trimmed': changed, 'emails': len(rows)}

    def purge_gmail_exclusions(self, account):
        terms = [term.casefold() for term in account.get('excluded_terms', []) if term]
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            source_ids = []
            for row in db.execute("SELECT source_id,title,body,metadata FROM events WHERE account_id=? AND kind='gmail.message'",
                                  (account['id'],)):
                if any(term in html.unescape(value).casefold() for term in terms
                       for value in [row['title'], row['body'], *json.loads(row['metadata']).values()]
                       if isinstance(value, str)):
                    source_ids.append(row['source_id'])
            return {'removed': self.exclude_sources(db, account['id'], source_ids)}

    def purge_email_subject_exclusions(self, config):
        """Remove already-stored emails whose subject the owner excluded; checkpoints untouched."""
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            removed = {}
            for row in db.execute("SELECT account_id,source_id,title FROM events WHERE kind IN ('gmail.message','salesflare.email')").fetchall():
                if email_subject_excluded(config, row['title']):
                    removed.setdefault(row['account_id'], []).append(row['source_id'])
            return {account: self.exclude_sources(db, account, ids, reason='email_subject_excluded')
                    for account, ids in removed.items()}

    def purge_calendar_exclusions(self, account):
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            source_ids = [r['source_id'] for r in db.execute(
                "SELECT source_id,title FROM events WHERE account_id=? AND kind='calendar.event'", (account['id'],))
                if calendar_title_excluded(account, r['title'])]
            return {'removed': self.exclude_sources(db, account['id'], source_ids,
                                                   reason='calendar_title_excluded')}

    @contextlib.contextmanager
    def connect(self):
        timing = getattr(_REQUEST_TIMING, 'value', None)  # a request being answered on this thread: its database time
        if timing is None:
            with self._connect() as db:
                yield db
            return
        started = time.monotonic()
        held = None
        try:
            with self._connect(timing, started) as db:
                held = time.monotonic()
                yield db
        finally:
            done = time.monotonic()
            timing['db_connections'] += 1
            timing['db_held'] += done - (held or done)
            if held is None:
                timing['db_wait'] += done - started

    @contextlib.contextmanager
    def _connect(self, timing=None, started=0.0):
        db = sqlite3.connect(self.path, timeout=20, factory=message_seal.Connection)
        db.row_factory = sqlite3.Row
        db.protected = self.protected
        if self.sealer:
            message_seal.attach(db, self.sealer)
            db.execute('PRAGMA secure_delete=ON')  # a deleted or replaced message leaves no copy in a free page
            if self.protected and db.execute('PRAGMA schema_version').fetchone()[0] != self._sealed_schema:
                # a table made since (a migration, joining a Fleet): its guards, and anything it got meanwhile
                with db:
                    message_seal.ensure_triggers(db)
                    sealed_now = message_seal.leftovers(db, seal=True)
                if sealed_now:  # their plain text leaves the log too (secure_delete already cleared the old cells)
                    LOG.info('message contents sealed in place: %s values', sealed_now)
                    db.execute('PRAGMA wal_checkpoint(TRUNCATE)')
                self._sealed_schema = db.execute('PRAGMA schema_version').fetchone()[0]
        db.execute('PRAGMA foreign_keys=ON')
        if timing is not None:  # opened and set up: waiting on a lock to read the schema counts here
            timing['db_wait'] += time.monotonic() - started
        try:
            with db:
                yield db
        finally:
            db.close()

    def checkpoint(self, account):
        with self.connect() as db:
            row = db.execute('SELECT state FROM checkpoints WHERE account_id=?', (account,)).fetchone()
            return json.loads(row[0]) if row else None
